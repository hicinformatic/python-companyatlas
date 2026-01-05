from providerkit import ProviderBase


class CompanyAtlasProvider(ProviderBase):
    config_prefix = "COMPANYATLAS"
    services = [
        "search_company",
        "search_company_by_code",
        "get_company_documents",
        "get_company_events",
        "get_company_officers",
        "get_ultimate_beneficial_owners",
    ]


__all__ = [CompanyAtlasProvider]