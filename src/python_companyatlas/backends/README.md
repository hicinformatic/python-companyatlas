# Backends System

Le système de backends permet de récupérer des données de companies/entities par pays.

## Structure

Les backends sont organisés par continent puis pays :

```
backends/
├── base.py                    # Classe de base générique
├── europe/
│   └── france/
│       ├── base.py            # Fonctions de base spécifiques à la France
│       ├── insee.py           # Backend INSEE SIRENE
│       ├── entdatagouv.py     # Backend data.gouv.fr (BODACC, BALO)
│       ├── pappers.py         # Backend Pappers (agrégateur de données)
│       ├── infogreffe.py      # Backend Infogreffe (registre du commerce)
│       ├── opendatasoft.py    # Backend Opendatasoft (plateforme open data)
│       ├── inpi.py            # Backend INPI (Institut National de la Propriété Industrielle)
│       ├── societecom.py      # Backend Societe.com (agrégateur)
│       ├── verif.py           # Backend Verif.com (vérification d'entreprises)
│       ├── societeinfo.py     # Backend SocieteInfo (enrichissement B2B)
│       ├── cci.py             # Backend CCI (Chambres de Commerce)
│       ├── societedata.py     # Backend SocieteData (données légales/financières)
│       ├── pharow.py          # Backend Pharow (agrégation B2B)
│       └── espacedocs.py      # Backend EspaceDocs (documents officiels)
```

## Utilisation

### Recherche par nom

Recherche générique par nom de société (ex: "tour eiffel") :

```python
from python_companyatlas.backends import INSEEBackend

backend = INSEEBackend(config={"api_key": "your_key"})
results = backend.search_by_name("tour eiffel", limit=10)
```

### Recherche par code d'enregistrement

Recherche spécifique par SIREN ou RNA :

```python
from python_companyatlas.backends import INSEEBackend, EntDataGouvBackend

# Recherche par SIREN
insee = INSEEBackend()
company = insee.search_by_code("123456789", code_type="siren")

# Recherche par RNA (associations)
datagouv = EntDataGouvBackend()
association = datagouv.search_by_code("W12345678", code_type="rna")

# Recherche avec Pappers (nécessite une clé API)
from python_companyatlas.backends import PappersBackend

pappers = PappersBackend(config={"api_key": "your_api_key"})
results = pappers.search_by_name("tour eiffel", limit=10, departement="75")

# Recherche avec Infogreffe
from python_companyatlas.backends import InfogreffeBackend

infogreffe = InfogreffeBackend()
company = infogreffe.search_by_code("123456789", code_type="siren")
kbis = infogreffe.get_extrait_kbis("123456789")

# Recherche avec Opendatasoft
from python_companyatlas.backends import OpendatasoftBackend

opendatasoft = OpendatasoftBackend()
results = opendatasoft.search_by_name("tour eiffel", active_only=True)
```

### Récupération de documents officiels

Récupération des publications BODACC et BALO :

```python
from python_companyatlas.backends import EntDataGouvBackend
from datetime import datetime, timedelta

backend = EntDataGouvBackend()

# Tous les documents
documents = backend.get_documents("123456789")

# Seulement BODACC
bodacc_docs = backend.get_documents(
    "123456789",
    document_type="bodacc",
    date_from=(datetime.now() - timedelta(days=365)).isoformat()
)

# Seulement BALO
balo_docs = backend.get_documents(
    "123456789",
    document_type="balo"
)
```

## Backends disponibles

### France

- **INSEEBackend** : Accès à la base SIRENE de l'INSEE
  - Recherche par nom
  - Recherche par SIREN
  - Données officielles des entreprises

- **EntDataGouvBackend** : Accès aux données de data.gouv.fr
  - Recherche par nom
  - Recherche par SIREN ou RNA
  - Publications BODACC et BALO

- **PappersBackend** : Agrégateur de données d'entreprises françaises
  - Recherche par nom avec filtres avancés (département, NAF, forme juridique)
  - Recherche par SIREN avec données complètes
  - Données financières
  - Documents officiels (BODACC, états financiers, documents légaux)
  - Informations sur les dirigeants et actionnaires

- **InfogreffeBackend** : Registre du commerce et des sociétés
  - Recherche par nom ou RCS
  - Recherche par SIREN
  - Extrait K-bis officiel
  - Documents légaux et publications BODACC
  - Informations sur les greffes

- **OpendatasoftBackend** : Plateforme open data
  - Recherche par nom dans plusieurs datasets
  - Recherche par SIREN
  - Accès aux publications BODACC et BALO
  - Accès à de multiples datasets publics
  - Possibilité de lister les datasets disponibles

- **INPIBackend** : Institut National de la Propriété Industrielle
  - Registre national des entreprises (commerciales, artisanales, agricoles, indépendantes)
  - Recherche par nom
  - Recherche par SIREN
  - Données officielles complètes

- **SocieteComBackend** : Agrégateur d'informations sur les entreprises
  - Informations légales, juridiques et financières
  - Agrège données INPI, INSEE, RCS
  - Recherche par nom et SIREN
  - Données financières et documents

- **VerifBackend** : Vérification d'entreprises
  - Vérification de données d'entreprises
  - Recherche par nom et SIREN
  - Services de validation

- **SocieteInfoBackend** : Enrichissement de données B2B
  - Services d'enrichissement de données
  - Bases de données BtoB
  - Données mises à jour quotidiennement
  - API entreprise

- **CCIBackend** : Chambres de Commerce et d'Industrie
  - Annuaire des Entreprises de France
  - Entreprises répertoriées par les CCI
  - Recherche par nom et SIREN

- **SocieteDataBackend** : Données légales, financières et stratégiques
  - Plus de 12 millions d'entreprises françaises
  - Données légales, financières et stratégiques
  - Informations sur dirigeants et bilans
  - Documents juridiques

- **PharowBackend** : Agrégation de sources de données B2B
  - Centralisation de diverses sources B2B
  - Enrichissement de données d'entreprises
  - Segmentations personnalisées

- **EspaceDocsBackend** : Documents officiels
  - Accès instantané aux informations officielles
  - Documents légaux, bilans financiers
  - K-bis, états financiers
  - Plus de 12 millions d'entreprises

## Interface commune

Tous les backends implémentent l'interface `BaseBackend` :

- `search_by_name(name: str, **kwargs) -> List[Dict[str, Any]]`
- `search_by_code(code: str, code_type: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]`
- `get_documents(identifier: str, document_type: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]`

