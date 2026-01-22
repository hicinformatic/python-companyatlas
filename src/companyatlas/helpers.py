from typing import Any, cast

from providerkit.helpers import call_providers, get_providers

from .providers import CompanyAtlasProvider

ADD_FIELDS = {
    "geo_data": {
        "label": "Data source",
        "description": "Data source",
        "format": "str",
    },
}

def get_companyatlas_providers(*args: Any, **kwargs: Any) -> dict[str, Any] | str:
    """Get companyatlas providers."""
    lib_name = kwargs.pop('lib_name', 'companyatlas')
    return cast('dict[str, Any] | str', get_providers(*args, lib_name=lib_name, add_fields=ADD_FIELDS, **kwargs))


def get_companyatlas_provider(attribute_search: dict[str, Any], *args: Any, **kwargs: Any) -> CompanyAtlasProvider:
    """Get companyatlas provider by attribute search."""
    lib_name = kwargs.pop('lib_name', 'companyatlas')
    providers = get_providers(*args, attribute_search=attribute_search, format="python", lib_name=lib_name, add_fields=ADD_FIELDS, **kwargs)
    if not providers:
        raise ValueError("No providers found")
    if len(providers) > 1:
        raise ValueError(f"Expected 1 provider, got {len(providers)}")
    return cast('CompanyAtlasProvider', providers[0])

def search_company(query: str, *args: Any, **kwargs: Any) -> Any:
    """Search company using providers."""
    return call_providers(
        *args,
        command="search_company",
        lib_name="companyatlas",
        query=query,
        **kwargs,
    )


def search_company_by_reference(code: str, *args: Any, **kwargs: Any) -> Any:
    """Search company by reference (SIREN, SIRET, RNA, etc.) using providers."""
    return call_providers(
        *args,
        command="search_company_by_reference",
        lib_name="companyatlas",
        code=code,
        **kwargs,
    )


def get_company_documents(code: str, *args: Any, **kwargs: Any) -> Any:
    """Get company documents using providers."""
    return call_providers(
        *args,
        command="get_company_documents",
        lib_name="companyatlas",
        code=code,
        **kwargs,
    )


def get_company_events(code: str, *args: Any, **kwargs: Any) -> Any:
    """Get company events using providers."""
    return call_providers(
        *args,
        command="get_company_events",
        lib_name="companyatlas",
        code=code,
        **kwargs,
    )


def get_company_officers(code: str, *args: Any, **kwargs: Any) -> Any:
    """Get company officers using providers."""
    return call_providers(
        *args,
        command="get_company_officers",
        lib_name="companyatlas",
        code=code,
        **kwargs,
    )


def get_ultimate_beneficial_owners(code: str, *args: Any, **kwargs: Any) -> Any:
    """Get ultimate beneficial owners using providers."""
    return call_providers(
        *args,
        command="get_ultimate_beneficial_owners",
        lib_name="companyatlas",
        code=code,
        **kwargs,
    )

