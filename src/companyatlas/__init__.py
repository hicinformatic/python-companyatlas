"""lib example - Example Python library with src/ structure."""

__version__ = "0.1.0"


COMPANYATLAS_SEARCH_COMPANY_FIELDS = {
    "denomination": {
        "label": "Denomination",
        "description": "Denomination",
        "format": "str",
    },
    "reference": {
        "label": "Reference",
        "description": "Reference",
        "format": "str",
    },
    "source_field": {
        "label": "Source field",
        "description": "Source field",
        "format": "str",
    },
    "country_code": {
        "label": "Country code",
        "description": "Country code",
        "format": "str",
    },
    "address": {
        "label": "Address",
        "description": "Address",
        "format": "str",
    },
    "address_json": {
        "label": "Address JSON",
        "description": "Address JSON",
        "format": "json",
    },
    "companyatlas_id": {
        "label": "Companyatlas ID",
        "description": "Companyatlas ID",
        "format": "str",
    },
    "data_source": {
        "label": "Data source",
        "description": "Data source",
        "format": "str",
    },
    "backend": {
        "label": "Backend display name",
        "description": "Backend display name",
        "format": "str",
    },
    "backend_name": {
        "label": "Simple backend name (e.g., insee)",
        "description": "Simple backend name (e.g., insee)",
        "format": "str",
    },
}

COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS = {
    "documents": {
        "label": "Documents",
        "description": "Documents",
        "format": "list",
    },
    "companyatlas_id": {
        "label": "Companyatlas ID",
        "description": "Companyatlas ID",
        "format": "str",
    },
}

COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS = {
    "events": {
        "label": "Events",
        "description": "Events",
        "format": "list",
    },
    "companyatlas_id": {
        "label": "Companyatlas ID",
        "description": "Companyatlas ID",
        "format": "str",
    },
}

COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS = {
    "officers": {
        "label": "Officers",
        "description": "Officers",
        "format": "list",
    },
    "companyatlas_id": {
        "label": "Companyatlas ID",
        "description": "Companyatlas ID",
        "format": "str",
    },
}

COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS = {
    "ultimate_beneficial_owners": {
        "label": "Ultimate beneficial owners",
        "description": "Ultimate beneficial owners",
        "format": "list",
    },
    "companyatlas_id": {
        "label": "Companyatlas ID",
        "description": "Companyatlas ID",
        "format": "str",
    },
}

COMPANYATLAS_GET_REFERENTIEL_FIELDS = {
    "category": {
        "label": "Category",
        "description": "Referentiel category",
        "format": "str",
    },
    "code": {
        "label": "Code",
        "description": "Referentiel code",
        "format": "str",
    },
    "description": {
        "label": "Description",
        "description": "Referentiel description",
        "format": "str",
    },
    "characteristics": {
        "label": "Characteristics",
        "description": "Referentiel characteristics",
        "format": "str",
    },
    "priority": {
        "label": "Priority",
        "description": "Referentiel priority",
        "format": "int",
    },
    "usage_type": {
        "label": "Usage Type",
        "description": "Usage type (description, configuration, characteristics)",
        "format": "str",
    },
}

__all__ = [
    "COMPANYATLAS_SEARCH_COMPANY_FIELDS",
    "COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS",
    "COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS",
    "COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS",
    "COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS",
    "COMPANYATLAS_GET_REFERENTIEL_FIELDS",
]
