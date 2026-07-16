# Migration from legacy `organization/` to `organizationatlas`

Comparison and roadmap to absorb the data model of the legacy `organization/` Django
app into the `organizationatlas` architecture without breaking its design.

## Architectures compared

| Aspect | `organization/` (legacy) | `organizationatlas/` (new) |
|---|---|---|
| Structure | Mono-app Django | Core Python + Django integration split |
| Providers | Ad-hoc `SearchBackend` hierarchy, 3 backends (INSEE, opendatasoft, entdatagouv) | ProviderKit providers, geo hierarchy (world → europe → france), 4 providers (+ INPI) |
| Models | `Organization` + `OrganizationFR` (concrete country-specific models) | EAV (`OrganizationAtlasData`) + country-agnostic base |
| Referentials | Hardcoded in `choices/fr.py` (3 758 lines: APE, LEGALFORM, …) | `OrganizationAtlasReferentiel` (DB) + CSV loader |
| Dependencies | `mighty.*`, `rest_framework` | `django_boosted`, `virtualqueryset`, `namedid`, `django_geoaddress` |
| Creation flow | `create_entity('fr', dict)` → Organization + OrganizationFR + Address | `VirtualOrganization.create_organization()` → Organization + 1 Data + 1 Address |

`organizationatlas` has a **better architecture** but **less business data coverage**.
The goal of this document is to map what `organization/` captures and explain where
it should land in `organizationatlas`.

## What `organization/` has that `organizationatlas/` is missing

### 1. Business fields on `Organization`

```python
parent = ForeignKey('self', ...)              # parent/subsidiary hierarchy
since = DateField(...)                         # creation date
site = URLField(...)
effective = BigIntegerField(...)               # headcount
secretary = CharField(...)
resume = RichTextField(...)
is_type = (COMPANY | ASSOCIATION | COOWNER | BIGMASTER)
purpose / instance_comex / matrix_skills       # qualitative governance
```

### 2. Financial / marketplace block

`turnover`, `net_profit`, `dividend`, `total_dividend`, `securities`, `current`,
`valorisation`, `nominal`, `share_capital`, `floating`, `is_capital_variable`,
`capital_division (JSON)`, `icb`, `market`, `dowjones`, `nasdaq`, `gaia`.

Many of these are **time-series** data (they change over time and need history).

### 3. Internal governance rules

`settle_internal`, `duration_mandate`, `age_limit_pdg`, `age_limit_dg`,
`stock_min_rule`, `stock_min_status`, `stackholder_kind`, `stock_kind`.

### 4. France-specific fields on `OrganizationFR`

`siren`, `siret`, `rna`, `ape`, `ape_noun`, `category`, `legalform`,
`slice_effective`, `effective`, `isin`, `ticker`, `coderef`, `index`,
`governance`, `evaluation`, `quality_independent`, `siege`.

### 5. Huge referentials in `choices/fr.py`

- **APE** — full NAF rev. 2 codes (thousands of entries)
- **LEGALFORM** — INSEE legal categories
- **SLICE_EFFECTIVE** — headcount brackets
- **GOVERNANCE**, **EVALUATION**, **INDEX**, **CODEREF**, **ICB**, **MARKET**
- **STACKHOLDER_DEFAULT** and **INSTRUMENTST** — `legalform code → kind`
  mappings (300+ entries each)

### 6. `Balo` model (legal announcements)

```python
class Balo(Base):
    organizationfr = ForeignKey(...)
    announce = CharField(choices=ANNOUNCE, ...)
    case = PositiveIntegerField()
    link, file_link = URLField()
    date = DateField()
```

### 7. Admin creation workflow

`organization/admin.py` exposes a custom flow: Actions → Countries → Search → Create
with custom views. `organizationatlas` has the Search and Create steps via
`OrganizationAtlasVirtualOrganizationAdmin` but no country routing.

### 8. Full country list + flags

`choices/countries.py` + 250 PNG flags in `static/flags/`.

## Implementation plan in `organizationatlas`

The point is **not to copy everything**. The EAV architecture of organizationatlas
can absorb 80 % of these fields without a new model. The layout below maps each
category of data to its target location.

### A. Stable, non-versioned fields → promote on `OrganizationAtlasOrganization`

These fields are user-edited, not source-derived:

```python
class OrganizationAtlasOrganization(OrganizationAtlasSourceBase):
    # existing
    denomination, code, named_id

    # to add
    parent = ForeignKey('self', null=True, blank=True, on_delete=SET_NULL,
                        related_name='children')
    is_type = CharField(choices=[COMPANY, ASSOCIATION, COOWNER, BIGMASTER])
    since = DateField(null=True, blank=True)
    site = URLField(blank=True)
    resume = TextField(blank=True)
```

### B. France-specific factual fields → `OrganizationAtlasData` (EAV)

`siren`, `siret`, `rna`, `ape`, `ape_noun`, `legalform`, `category`,
`slice_effective`, `effective`, `isin`, `ticker`, `index`, `coderef`,
`governance`, `evaluation`, `quality_independent`, `phone`.

Uses the existing pattern:

```python
OrganizationAtlasData.objects.create(
    organization=c, source='insee', country_code='FR',
    data_type='siren', value_type='str', value='123456789',
    referentiel=[<OrganizationAtlasReferentiel: ape/1234>]  # if applicable
)
```

**Major benefit:** INSEE and INPI can give different values for the same
`data_type`. The existing
`unique_together = [organization, source, country_code, data_type]` already supports
multi-source storage with provenance.

### C. Choices/referentials → `OrganizationAtlasReferentiel` + CSV

Convert every `choices/fr.py` group into a CSV loaded by `referentiel --import`:

```
referentiel/import/
├─ ape.csv
├─ legalform.csv
├─ slice_effective.csv
├─ governance.csv
├─ evaluation.csv
├─ index.csv
├─ coderef.csv
├─ icb.csv
├─ market.csv
└─ stackholder_mapping.csv      # 5192 → ADHERENT, etc.
```

`OrganizationAtlasReferentiel` already has:

- `category` (e.g. `"ape"`, `"legalform"`…)
- `code` (e.g. `"1000"`, `"EURONEXT_GROWTH"`…)
- `description` + `characteristics` + `usage_type`

The `referentiel --import` management command scans a folder and ingests every
`*.csv` it finds.

### D. Financial block → new `OrganizationAtlasFinancial` model

Financial data has a **time dimension** that `OrganizationAtlasData` does not model
(2023 turnover vs 2024 turnover). Dedicated model:

```python
class OrganizationAtlasFinancial(OrganizationAtlasSourceBase):
    organization = ForeignKey(OrganizationAtlasOrganization, related_name='financials')
    indicator = CharField(choices=[
        'turnover', 'net_profit', 'valorisation', 'dividend',
        'share_capital', 'floating', 'current', 'securities', 'nominal', ...
    ])
    period_start = DateField()
    period_end = DateField(null=True)
    value = DecimalField(max_digits=20, decimal_places=4)
    currency = CharField(max_length=3, default='EUR')

    # capital_division (JSON in legacy `organization`)
    breakdown = JSONField(null=True, blank=True)

    class Meta:
        unique_together = [organization, indicator, period_start, source]
```

### E. Governance rules → new `OrganizationAtlasGovernance` (OneToOne)

These are **user-configured** parameters, not source-derived. They do not fit
the EAV story:

```python
class OrganizationAtlasGovernance(models.Model):
    organization = OneToOneField(OrganizationAtlasOrganization, related_name='governance')
    settle_internal = BooleanField(default=False)
    duration_mandate = PositiveSmallIntegerField(null=True)
    age_limit_pdg = BooleanField(default=False)
    age_limit_dg = BooleanField(default=False)
    stock_min_rule = PositiveIntegerField(null=True)
    stock_min_status = PositiveIntegerField(null=True)
    stackholder_kind = CharField(choices=STACKHOLDER_KINDS)
    stock_kind = CharField(choices=STOCK_KINDS)
    purpose = CharField(choices=YESNO, null=True)
    instance_comex = BooleanField(default=False)
    matrix_skills = BooleanField(default=False)
```

### F. Marketplace listing → `OrganizationAtlasListing` (OneToOne, FR-scoped)

`icb`, `market`, `dowjones`, `nasdaq`, `gaia`, `index`, `coderef` only matter
for listed organizations. Keep them isolated in a OneToOne or a JSONField on
`Organization`.

### G. Balo → reuse `OrganizationAtlasEvent`

No dedicated model needed:

| `Balo` field | `OrganizationAtlasEvent` mapping |
|---|---|
| `announce` | `metadata.announce_code` |
| announce label | `title` |
| `case` | `metadata.case` |
| `link` | `url` |
| `file_link` | `metadata.file_link` |
| `date` | `date` |
| — | `event_type = "balo"` |

### H. Enriched `create_organization()`

```python
@transaction.atomic
def create_organization(obj):
    organization = OrganizationAtlasOrganization.objects.create(
        denomination=obj.denomination,
        code=obj.reference,
        is_type='ASSOCIATION' if obj.source_field == 'rna' else 'COMPANY',
        since=getattr(obj, 'since', None),
    )
    # Persist every relevant field from the raw source response
    raw = obj.raw or {}
    for data_type, value in extract_fr_data(raw).items():
        OrganizationAtlasData.objects.update_or_create(
            organization=organization,
            source=obj.backend,
            country_code='FR',
            data_type=data_type,
            defaults={'value': value, 'value_type': infer_type(value)},
        )
    if obj.address_json:
        OrganizationAtlasAddress.objects.create(...)
    return organization
```

This requires exposing `raw` on `OrganizationAtlasVirtualOrganization` (see
[`source-response-access`](#raw-source-access) below).

### I. Admin "search by country" workflow

`organization/` exposes Actions → Countries → Search → Create.

`organizationatlas` already has:

- `OrganizationAtlasVirtualOrganizationAdmin` with `BackendServiceAdminFilter`
  (= choose the provider)
- "Create Organization" button via `changeform_actions`

What is missing is the intermediate "choose a country" screen, which is only
useful when more than one country is implemented. Defer until a non-FR provider
exists.

## What to leave behind

- **`mighty.*` dependencies** (`Base`, `Image`, `BaseAdmin`, `Address`,
  `RichTextField`) — replaced by `django_boosted` / `django_geoaddress`.
- **`maskedSerializer`** — unless a public DRF API is needed.
- **Country choices + flags PNG** — `django-countries` is better.
- **Python-side `STACKHOLDER_DEFAULT` / `INSTRUMENTST` mappings** — load them
  into `OrganizationAtlasReferentiel` instead.
- **`default_app_config`** — deprecated since Django 3.2.
- **`decorators.py`** (empty file).
- **Dedicated `Balo` model** — covered by `OrganizationAtlasEvent`.

## Raw source access

The `raw` source response is already preserved at four points in `providerkit`
(see `providerkit/kit/__init__.py:190-204` and `providerkit/kit/service.py`).
To expose it as a Django model field, declare a `raw` JSON field in the schemas
of `organizationatlas/__init__.py` and in the corresponding `VirtualModel`. No
changes needed in `providerkit` or `django-providerkit`.

## Roadmap

| Priority | Task | Effort |
|---|---|---|
| 1 | Add `parent`, `is_type`, `since`, `site`, `resume` on `OrganizationAtlasOrganization` | 10 min |
| 2 | Convert `choices/fr.py` (APE, LEGALFORM, SLICE_EFFECTIVE, …) to CSV in `data_sources/fr/` | ~1h (conversion script) |
| 3 | Extend `referentiel --import` to scan a folder | 20 min |
| 4 | Enrich `create_organization()` to push all `raw` fields into `OrganizationAtlasData` | 30 min |
| 5 | Create `OrganizationAtlasFinancial` (model + admin) | 1h |
| 6 | Create `OrganizationAtlasGovernance` (OneToOne) | 30 min |
| 7 | Create `OrganizationAtlasListing` (OneToOne FR) — optional | 30 min |
| 8 | Verify `Balo` is covered by `Event` and adapt INPI provider to emit it | 1h |

Steps **1–4** unlock the most value (data coverage parity with `organization` for
the search/create flow). Steps **5–8** are additive and can be done later
without breaking the architecture.
