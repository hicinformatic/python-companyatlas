# python-companyatlas

Company information lookup and enrichment library.

## Installation

```bash
pip install python-companyatlas
```

## Development

```bash
# Create virtual environment
python dev.py venv

# Install dependencies
python dev.py install

# Run tests
python dev.py test

# Run linters
python dev.py lint

# Format code
python dev.py format
```

## Usage

```python
from python_companyatlas import CompanyAtlas

# Example usage
atlas = CompanyAtlas()
company = atlas.lookup("example.com")
print(company.name)
```

## License

MIT

