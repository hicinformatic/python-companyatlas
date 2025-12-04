# Provider System

## Overview

python-companyatlas collects company information from official sources organized by country. Providers are structured in a **continent/country** hierarchy.

## Directory Structure

```
src/python_companyatlas/providers/
├── __init__.py                      # BaseProvider interface
├── europe/
│   ├── __init__.py
│   ├── france/
│   │   ├── __init__.py
│   │   ├── infogreffe.py           # French commercial court registry
│   │   ├── pappers.py              # French company aggregator
│   │   └── sirene.py               # INSEE SIRENE database
│   ├── germany/
│   │   ├── __init__.py
│   │   └── handelsregister.py      # German commercial register
│   └── uk/
│       ├── __init__.py
│       └── companies_house.py      # UK Companies House
├── americas/
│   ├── __init__.py
│   └── usa/
│       ├── __init__.py
│       └── sec.py                  # US SEC EDGAR database
└── asia/
    ├── __init__.py
    └── ...
```

## Data Types Collected

Each provider can collect one or more of the following:

### 1. **Addresses**
- Headquarters
- Branches
- Registered office
- Historical addresses

### 2. **Subsidiaries**
- Parent/child relationships
- Ownership percentages
- Corporate structure

### 3. **Documents**
- Registration certificates
- Financial statements
- Legal notices
- Annual reports

### 4. **Identifiers**
- Country-specific registration numbers (SIREN, CRN, etc.)
- VAT numbers
- Industry codes (NACE, NAF, SIC)

## Provider Interface

All providers must implement `BaseProvider`:

```python
from python_companyatlas.providers import BaseProvider

class MyProvider(BaseProvider):
    name = "my_provider"
    country_code = "FR"  # ISO 3166-1 alpha-2
    supported_data_types = ["addresses", "subsidiaries", "documents"]
    
    def __init__(self, config=None):
        self.config = config or {}
        self.api_key = self.config.get("api_key")
    
    def lookup_by_identifier(self, identifier, identifier_type):
        """Look up company by identifier."""
        ...
    
    def get_addresses(self, identifier):
        """Get all company addresses."""
        ...
    
    def get_subsidiaries(self, identifier):
        """Get company subsidiaries."""
        ...
    
    def get_documents(self, identifier):
        """Get official documents."""
        ...
```

## Adding a New Provider

1. **Choose the correct location**:
   ```
   providers/{continent}/{country}/provider_name.py
   ```

2. **Implement BaseProvider**:
   - Set `name`, `country_code`, and `supported_data_types`
   - Implement all required methods
   - Handle rate limiting and errors

3. **Add configuration**:
   - Support API keys via config dict
   - Never hardcode credentials
   - Document required config keys

4. **Write tests**:
   ```python
   # tests/test_providers_europe_france.py
   def test_french_provider_lookup():
       provider = FrenchProvider(config={"api_key": "test"})
       result = provider.lookup_by_identifier("123456789", "siren")
       assert result["country"] == "FR"
   ```

5. **Document the source**:
   - Official registry URL
   - API documentation
   - Data coverage and limitations

## Country-Specific Identifiers

### France
- **SIREN**: 9-digit company identifier
- **SIRET**: 14-digit establishment identifier (SIREN + NIC)
- **VAT**: FR + 2 digits + SIREN

### Germany
- **HRB/HRA**: Commercial register number
- **VAT**: DE + 9 digits

### United Kingdom
- **CRN**: Company Registration Number (8 digits)
- **VAT**: GB + 9 or 12 digits

### United States
- **EIN**: Employer Identification Number (9 digits)
- **CIK**: SEC Central Index Key
- **State registration**: Varies by state

## Best Practices

1. **Rate Limiting**: Always respect API rate limits
2. **Caching**: Cache responses to reduce API calls
3. **Error Handling**: Return meaningful errors
4. **Data Validation**: Validate identifiers before API calls
5. **Documentation**: Document data sources and limitations
6. **Testing**: Mock external APIs in tests

## Example Usage

```python
from python_companyatlas import CompanyAtlas

# Initialize with configuration
atlas = CompanyAtlas(config={
    "providers": {
        "europe/france/infogreffe": {
            "api_key": "your_key"
        }
    }
})

# Look up a French company by SIREN
company = atlas.lookup("123456789", country="FR", identifier_type="siren")

# Get addresses
addresses = company.get("addresses", [])

# Get subsidiaries
subsidiaries = company.get("subsidiaries", [])
```

## Resources

- [ISO 3166-1 Country Codes](https://en.wikipedia.org/wiki/ISO_3166-1_alpha-2)
- [NACE Industry Codes](https://ec.europa.eu/eurostat/web/nace)
- [OpenCorporates API](https://api.opencorporates.com/)

