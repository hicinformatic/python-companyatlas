"""lib example - Example Python library with src/ structure."""

__version__ = "0.1.0"


COMPANYATLAS_SEARCH_COMPANY_FIELDS = {
    "denomination": {
        "label": "Name",
        "description": "Name",
        "format": "str",
    },
    "country": {
        "label": "Country",
        "description": "Country",
        "format": "str",
    },
    "data_source": {
        "label": "Data source",
        "description": "Data source",
        "format": "str",
    },
}

COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS = {
    "documents": {
        "label": "Documents",
        "description": "Documents",
        "format": "list",
    },
}

COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS = {
    "events": {
        "label": "Events",
        "description": "Events",
        "format": "list",
    },
}

COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS = {
    "officers": {
        "label": "Officers",
        "description": "Officers",
        "format": "list",
    },
}

COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS = {
    "ultimate_beneficial_owners": {
        "label": "Ultimate beneficial owners",
        "description": "Ultimate beneficial owners",
        "format": "list",
    },
}

__all__ = [
    "COMPANYATLAS_SEARCH_COMPANY_FIELDS",
    "COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS",
    "COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS",
    "COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS",
    "COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS",
]
