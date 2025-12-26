from providerkit import ProviderBase


class CompanyAtlasProvider(ProviderBase):
    config_prefix = "COMPANYATLAS"
    services = [
        "search_company",
        "search_company_by_code",
        "download_company_documents",
        "get_company_events",
    ]


__all__ = [CompanyAtlasProvider]