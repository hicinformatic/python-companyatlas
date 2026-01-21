from providerkit import ProviderBase

from companyatlas import (
    COMPANYATLAS_SEARCH_COMPANY_FIELDS,
    COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS,
    COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS,
    COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS,
    COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS,
)


class CompanyAtlasProvider(ProviderBase):
    config_prefix = "COMPANYATLAS"
    services_cfg = {
        "search_company": {
            "label": "Search company",
            "description": "Search company",
            "format": "str",
            "fields": COMPANYATLAS_SEARCH_COMPANY_FIELDS,
        },
        "search_company_by_reference": {
            "label": "Search company by reference",
            "description": "Search company by reference",
            "format": "str",
            "fields": COMPANYATLAS_SEARCH_COMPANY_FIELDS,
        },
        "get_company_documents": {
            "label": "Get company documents",
            "description": "Get company documents",
            "format": "str",
            "fields": COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS,
        },
        "get_company_events": {
            "label": "Get company events",
            "description": "Get company events",
            "format": "str",
            "fields": COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS,
        },
        "get_company_officers": {
            "label": "Get company officers",
            "description": "Get company officers",
            "format": "str",
            "fields": COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS,
        },
        "get_ultimate_beneficial_owners": {
            "label": "Get ultimate beneficial owners",
            "description": "Get ultimate beneficial owners",
            "format": "str",
            "fields": COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS,
        },
    }


__all__ = [CompanyAtlasProvider]