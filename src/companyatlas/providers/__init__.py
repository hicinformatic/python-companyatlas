from __future__ import annotations

from typing import Any

from providerkit import ProviderBase

from .. import (
    COMPANYATLAS_GET_COMPANY_DOCUMENTS_FIELDS,
    COMPANYATLAS_GET_COMPANY_EVENTS_FIELDS,
    COMPANYATLAS_GET_COMPANY_OFFICERS_FIELDS,
    COMPANYATLAS_GET_ULTIMATE_BENEFICIAL_OWNERS_FIELDS,
    COMPANYATLAS_SEARCH_COMPANY_FIELDS,
)


class CompanyAtlasProvider(ProviderBase):
    geo_zone = "world"
    geo_country = "world"
    geo_code = "ww"
    config_prefix = "COMPANYATLAS"
    _default_services_cfg = {
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

    @property
    def geo_data(self) -> str:
        return f"{self.geo_zone}/{self.geo_country} ({self.geo_code})"

    def get_normalize_country(self, data: dict[str, Any]) -> str:
        return self.geo_data

    def get_normalize_data_source(self, data: dict[str, Any]) -> str:
        return str(data)

    def response(self, *args: Any, **kwargs: Any) -> str:
        readable = kwargs.pop('readable', False)
        command = args[0]
        mode = args[2]
        if readable and mode == 'terminal':
            del self.services_cfg[command]['fields']['data_source']
        return super().response(*args, **kwargs)


__all__ = ['CompanyAtlasProvider']
