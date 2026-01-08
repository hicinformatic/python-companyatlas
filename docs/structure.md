## Project Structure

CompanyAtlas follows a standard Python package structure with a provider-based architecture using ProviderKit for provider management.

### General Structure

```
python-companyatlas/
├── src/
│   └── companyatlas/          # Main package directory
│       ├── __init__.py        # Package exports
│       ├── providers/         # Company data provider implementations
│       │   ├── __init__.py    # CompanyAtlasProvider base class
│       │   └── ...            # Provider implementations
│       ├── commands/           # Command infrastructure
│       ├── helpers.py          # Helper functions (get_company_providers, search_companies, etc.)
│       ├── cli.py              # CLI interface
│       └── __main__.py         # Entry point for package execution
├── tests/                     # Test suite
│   └── ...
├── docs/                      # Documentation
│   └── ...
├── service.py                 # Main service entry point script
├── pyproject.toml             # Project configuration
└── ...
```

### Module Organization Principles

- **Single Responsibility**: Each module should have a clear, single purpose
- **Separation of Concerns**: Keep different concerns in separate modules
- **Provider-Based Architecture**: Providers inherit from ProviderKit's ProviderBase
- **Clear Exports**: Use `__init__.py` to define public API
- **Logical Grouping**: Organize related functionality together

### Provider Organization

The `providers/` directory contains company data provider implementations:

- **`__init__.py`**: Defines `CompanyAtlasProvider` base class that extends `ProviderBase` from ProviderKit
- Each provider file implements a specific company data service
- All providers inherit from `CompanyAtlasProvider` which provides common functionality

### Helper Functions

The `helpers.py` module provides:
- `get_company_providers()`: Get company providers from various sources
- `search_companies()`: Search companies using providers
- `get_company_by_reference()`: Get company by reference ID

### Package Exports

The public API is defined in `src/companyatlas/__init__.py`:
- Provider base class and helper functions

### ProviderKit Integration

CompanyAtlas uses ProviderKit for provider management:
- Providers inherit from `ProviderBase` via `CompanyAtlasProvider`
- Uses ProviderKit's helper functions for provider discovery and management
- Providers can be loaded from JSON, configuration, or directory scanning
