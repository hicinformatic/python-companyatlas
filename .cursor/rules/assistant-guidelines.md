## Assistant Guidelines

### Project Purpose

**python-companyatlas** is a library for collecting company information by country. It aggregates data from various official and commercial sources to provide:
- Company addresses and locations
- Subsidiaries and corporate structure
- Official documents (registrations, financial reports, certifications)
- Company identifiers (SIREN, VAT, registration numbers)
- Business activity and industry classifications

### Provider Organization

Providers/adapters are organized by **continent/country** hierarchy:
```
python_companyatlas/
└── providers/
    ├── europe/
    │   ├── france/
    │   │   ├── infogreffe.py      # French commercial court registry
    │   │   ├── pappers.py          # French company data aggregator
    │   │   └── sirene.py           # French SIRENE database
    │   ├── germany/
    │   │   └── handelsregister.py  # German commercial register
    │   └── uk/
    │       └── companies_house.py  # UK Companies House
    ├── americas/
    │   └── usa/
    │       └── sec.py              # US SEC EDGAR database
    └── asia/
        └── ...
```

Each provider must implement a common interface for consistency across countries.

### Development Guidelines

- Always execute project tooling through `python dev.py <command>`.
- Default to English for all code artifacts (comments, docstrings, logging, error strings, documentation snippets, etc.) regardless of the language used in discussions.
- Keep comments minimal and only when they clarify non-obvious logic.
- Avoid reiterating what the code already states clearly.
- Add comments only when they resolve likely ambiguity or uncertainty.
- Do not introduce any dependency on Django or other web frameworks (imports, settings, or implicit coupling).
- When adding helper-style utilities or tests, review `python_companyatlas/client.py` and helper modules for existing shortcuts before introducing new logic.
- **Testing**: Use pytest for all tests. Place tests in `tests/` directory with meaningful names (`test_client.py`, `test_enrichment.py`, etc.).
- **Type Hints**: All public functions and methods must have complete type hints.
- **Docstrings**: Use Google-style docstrings for all public classes, methods, and functions.
- **API Providers**: When adding new data providers or enrichment sources:
  - Create a module in `python_companyatlas/providers/{continent}/{country}/provider_name.py`
  - Follow the continent/country hierarchy strictly (e.g., `providers/europe/france/infogreffe.py`)
  - Implement a common interface (BaseProvider) for consistency across all countries
  - Each provider must specify its supported data types (addresses, subsidiaries, documents, identifiers)
  - Add configuration support via environment variables or config dict
  - Never hardcode API keys or credentials
  - Always handle rate limiting and errors gracefully
  - Document the official source (government registry, commercial API, etc.)
- **Data Validation**: Always validate input data (company domains, identifiers, etc.) before making external API calls.
- **Error Handling**: Use custom exceptions in `python_companyatlas/exceptions.py` for domain-specific errors.
- **Caching**: Consider implementing caching for expensive API calls to improve performance.
- **Geographic Data**: If dealing with company locations:
  - Use ISO country codes (ISO 3166-1 alpha-2)
  - Store coordinates as decimal degrees (latitude, longitude)
  - Include timezone information when relevant
- **Company Identifiers**: Support multiple identifier types per country:
  - Domain names (universal)
  - Company registration numbers (SIREN for France, CRN for UK, etc.)
  - VAT numbers (intra-community)
  - Stock symbols for public companies
  - Country-specific identifiers (follow local standards)
- **Data Privacy**: Never log sensitive company information (financial data, contact details, etc.).
- **Data Collection Capabilities**: Each provider should clearly document what it can collect:
  - **Addresses**: Headquarters, branches, registered office
  - **Subsidiaries**: Parent/child relationships, ownership percentages
  - **Documents**: Registration certificates, financial statements, legal notices
  - **Identifiers**: All official company numbers and codes
  - **Activity**: Business sectors, NACE/NAF codes, employee counts
- **Provider Discovery**: Never hardcode the list of providers. Always resolve via dynamic loading based on country/continent hierarchy.

