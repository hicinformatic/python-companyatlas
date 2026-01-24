# AI Assistant Contract — CompanyAtlas

**This document is the single source of truth for all AI-generated work in this repository.**  
All instructions in this file **override default AI behavior**.

Any AI assistant working on this project **must strictly follow this document**.

If a request conflicts with this document, **this document always wins**.

---

## Rule Priority

Rules in this document have the following priority order:

1. **ABSOLUTE RULES** — must always be followed, no exception
2. **REQUIRED RULES** — mandatory unless explicitly stated otherwise
3. **RECOMMENDED PRACTICES** — should be followed unless there is a clear reason not to
4. **INFORMATIONAL SECTIONS** — context and reference only

---

## ABSOLUTE RULES

These rules must always be followed.

- Follow this `AI.md` file exactly
- Do not invent new services, commands, abstractions, patterns, or architectures
- Do not refactor, redesign, or optimize unless explicitly requested
- Do not manipulate `sys.path`
- Do not use filesystem-based imports to access `providerkit` or `qualitybase`
- Do not hardcode secrets, credentials, tokens, or API keys
- Do not execute tooling commands outside the approved entry points
- **Comments**: Only add comments to resolve ambiguity or uncertainty. Do not comment obvious code.
- **Dependencies**: Add dependencies only when absolutely necessary. Prefer standard library always.
- If a request violates this document:
  - Stop
  - Explain the conflict briefly
  - Ask for clarification

---

## REQUIRED RULES

### Language and Communication

- **Language**: English only
  - Code
  - Comments
  - Docstrings
  - Logs
  - Error messages
  - Documentation
- Be concise, technical, and explicit
- Avoid unnecessary explanations unless requested

### Code Simplicity and Minimalism

- **Write the simplest possible code**: Always choose the simplest solution that works
- **Minimal dependencies**: Add dependencies only when absolutely necessary. Prefer standard library. Only add when essential functionality cannot be reasonably implemented otherwise
- **Minimal comments**: Comments only to resolve ambiguity or uncertainty. Do not comment obvious code or reiterate what the code already states clearly
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity or abstraction

---

## Project Overview (INFORMATIONAL)

**CompanyAtlas** is a Python library for company information lookup and enrichment. It provides a unified interface to multiple company data providers (INSEE, INPI, Entdatagouv, etc.) using ProviderKit for provider management.

### Core Functionality

1. **Search companies** with multiple data providers:
   - Company lookup by name, domain, or identifier
   - Company information enrichment
   - Company data validation and normalization
   - Get company by reference ID (SIREN, SIRET, RNA, etc.)
   - Get company documents, events, officers, and beneficial owners

2. **Manage multiple providers** through ProviderKit:
   - Provider discovery and enumeration
   - Provider selection and fallback mechanisms
   - Configuration management per provider
   - Dependency validation (API keys, packages)

3. **Standardized company format**:
   - Consistent company field structure across all providers
   - Field descriptions for company components
   - Support for international companies
   - Structured company data (name, domain, industry, location, etc.)

### Supported Providers

**French providers**: INSEE, INPI, Entdatagouv, Huwise

---

## Architecture (REQUIRED)

- Provider-based architecture built on ProviderKit
- Each company data service is implemented as a provider inheriting from `CompanyAtlasProvider`
- `CompanyAtlasProvider` extends `ProviderBase` from ProviderKit
- Providers are organized in the `providers/` directory
- Common functionality is shared through the base `CompanyAtlasProvider` class
- Provider discovery and management is handled by ProviderKit

---

## Project Structure (INFORMATIONAL)

```
python-companyatlas/
├── src/companyatlas/        # Main package
│   ├── providers/           # Company data provider implementations
│   ├── commands/            # Command infrastructure
│   ├── helpers.py           # Helper functions
│   └── cli.py               # CLI interface
├── tests/                   # Test suite
├── docs/                    # Documentation
├── service.py               # Main service entry point
└── pyproject.toml           # Project configuration
```

### Key Directories

- `src/companyatlas/providers/`: Company data provider implementations
- `src/companyatlas/commands/`: Command infrastructure for CLI system
- `tests/`: All tests using pytest

---

## Command Execution (ABSOLUTE)

- **Always use**: `./service.py dev <command>` or `python dev.py <command>`
- **Always use**: `./service.py quality <command>` or `python quality.py <command>`
- Never execute commands directly without going through these entry points

---

## Code Standards (REQUIRED)

### Typing and Documentation

- All public functions and methods **must** have complete type hints
- Use **Google-style docstrings** for:
  - Public classes
  - Public methods
  - Public functions
- Document raised exceptions in docstrings where relevant

### Testing

- Use **pytest** exclusively
- All tests must live in the `tests/` directory
- New features and bug fixes require corresponding tests

### Linting and Formatting

- Follow **PEP 8**
- Use configured tools:
  - `ruff`
  - `mypy`
- Use the configured formatter:
  - `ruff format`

---

## Code Quality Principles (REQUIRED)

- **Simplicity first**: Write the simplest possible solution. Avoid complexity unless clearly necessary.
- **Minimal dependencies**: Minimize dependencies to the absolute minimum. Only add when essential functionality cannot be reasonably implemented otherwise. Always prefer standard library.
- **No over-engineering**: Do not add abstractions, patterns, or layers unless they solve a real problem or are clearly needed.
- **Comments**: Comments are minimal and only when they resolve ambiguity or uncertainty. Do not comment what the code already states clearly. Do not add comments that reiterate obvious logic.
- **Separation of concerns**: One responsibility per module
- **Good factorization**: Factorize code when it improves clarity and reduces duplication, but only if it doesn't add unnecessary complexity

---

## Module Organization (REQUIRED)

- Single Responsibility Principle
- Logical grouping of related functionality
- Clear public API via `__init__.py`
- Avoid circular dependencies
- Provider-based architecture: Keep providers in separate files

---

## ProviderKit Integration (ABSOLUTE)

- `providerkit` is an installed package
- Always use standard Python imports:
  - `from providerkit import ProviderBase`
  - `from providerkit.helpers import get_providers, call_providers`
- Never manipulate import paths
- Never use file-based or relative imports to access `providerkit`
- For dynamic imports, use:
  - `importlib.import_module()` from the standard library

---

## Qualitybase Integration (ABSOLUTE)

- `qualitybase` is an installed package (used via service.py)
- Always use standard Python imports from `qualitybase.services` when needed
- No path manipulation: Never manipulate `sys.path` or use file paths to import qualitybase modules
- Direct imports only: Use `from qualitybase.services import ...` or `import qualitybase.services ...`
- Standard library imports: Use `importlib.import_module()` from the standard library if needed for dynamic imports
- Works everywhere: Since qualitybase is installed in the virtual environment, imports work consistently across all projects

---

## Provider Development (REQUIRED)

### Creating Providers

Providers must inherit from `CompanyAtlasProvider`:

```python
from companyatlas.providers import CompanyAtlasProvider

class MyProvider(CompanyAtlasProvider):
    name = "my_provider"
    display_name = "My Provider"
    description = "Description of my provider"
    required_packages = ["requests"]
    config_keys = ["MY_PROVIDER_API_KEY"]
    config_defaults = {"MY_PROVIDER_API_KEY": None}
    config_prefix = "MY_PROVIDER"
    services = ["search_company", "search_company_by_reference", "get_company_documents", "get_company_events"]
```

### Required Services

All providers must implement:
- `search_company(query: str, **kwargs)`: Search for companies by query string
- `search_company_by_reference(code: str, **kwargs)`: Get company by reference ID (SIREN, SIRET, RNA, etc.)
- `get_company_documents(code: str, **kwargs)`: Get company documents (if supported)
- `get_company_events(code: str, **kwargs)`: Get company events (if supported)
- `get_company_officers(code: str, **kwargs)`: Get company officers (if supported)
- `get_ultimate_beneficial_owners(code: str, **kwargs)`: Get ultimate beneficial owners (if supported)

### Company Format Standardization

- All providers must return companies in the standardized format defined by `COMPANYATLAS_SEARCH_COMPANY_FIELDS`
- Map provider's native response format to standard company format
- Use `None` or empty strings for missing optional fields
- Never omit required fields
- Store company data with appropriate types and precision

---

## Environment Variables (REQUIRED)

- `ENVFILE_PATH`
  - Path to `.env` file to load automatically
  - Relative to project root if not absolute
- `ENSURE_VIRTUALENV`
  - Set to `1` to automatically activate `.venv` if it exists
- Provider-specific variables:
  - Use provider-specific prefixes (e.g., `INSEE_`, `INPI_`, `ENTDATAGOUV_`, etc.)
  - Never hardcode API keys in code

---

## Error Handling (REQUIRED)

- Always handle errors gracefully
- Use appropriate exception types
- Provide clear, actionable error messages
- Do not swallow exceptions silently
- Document exceptions in docstrings where relevant
- Handle API rate limits and failures with proper retry logic when appropriate
- Support provider fallback mechanisms for resilience

---

## Configuration and Secrets (ABSOLUTE)

- Never hardcode:
  - API keys
  - Credentials
  - Tokens
  - Secrets
- Use environment variables or configuration files
- Use provider-specific configuration prefixes
- Clearly document required configuration

---

## Versioning (REQUIRED)

- Follow **Semantic Versioning (SemVer)**
- Update versions appropriately
- Clearly document breaking changes

---

## CLI System (INFORMATIONAL)

CompanyAtlas discovers commands from:

1. `commands/` directory
2. `.commands.json` configuration file

### Command Creation Rules (REQUIRED)

- Use `Command` class from `commands.base` **or**
- Define functions ending with `_command`
- Commands must:
  - Accept `args: list[str]`
  - Return `bool` (success / failure)

---

## Anti-Hallucination Clause (ABSOLUTE)

If a requested change is:
- Not supported by this document
- Not clearly aligned with the existing codebase
- Requiring assumptions or invention

You must:
1. Stop
2. Explain what is unclear or conflicting
3. Ask for clarification

Do not guess. Do not invent.

---

## Quick Compliance Checklist

Before producing output, ensure:

- [ ] All rules in `AI.md` are respected
- [ ] No forbidden behavior is present
- [ ] Code is simple, minimal, and explicit (simplest possible solution)
- [ ] Dependencies are minimal (prefer standard library)
- [ ] Comments only resolve ambiguity (no obvious comments)
- [ ] Code is well-factorized when it improves clarity (without adding complexity)
- [ ] Imports follow ProviderKit and Qualitybase rules
- [ ] Public APIs are typed and documented
- [ ] Providers inherit from CompanyAtlasProvider correctly
- [ ] Providers implement all required services
- [ ] Company format follows standardization (COMPANYATLAS_SEARCH_COMPANY_FIELDS)
- [ ] No API keys or secrets are hardcoded
- [ ] Tests are included when required
- [ ] Error handling is graceful with fallback support

---

## Additional Resources (INFORMATIONAL)

- `purpose.md`: Detailed project purpose and goals
- `structure.md`: Detailed project structure and module organization
- `development.md`: Development guidelines and best practices
- `README.md`: General project information

