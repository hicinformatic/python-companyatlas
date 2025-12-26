from pathlib import Path
from typing import Any

from providerkit.helpers import get_providers, try_providers, try_providers_first


def get_companyatlas_providers(
    *,
    json: str | Path | None = None,
    lib_name: str = "companyatlas",
    config: list[dict[str, Any]] | None = None,
    dir_path: str | Path | None = None,
    base_module: str | None = None,
    query_string: str | None = None,
    search_fields: list[str] | None = None,
    attribute_search: dict[str, str] | None = None,
    format: str | None = None,
) -> dict[str, Any] | str:
    """Get address providers."""
    providers = get_providers(  # type: ignore[no-any-return]
        json=json,
        lib_name=lib_name,
        config=config,
        dir_path=dir_path,
        base_module=base_module,
        query_string=query_string,
        search_fields=search_fields,
        attribute_search=attribute_search,
        format=format,
    )
    if not len(providers):
        raise ValueError("No providers found")
    return providers


def get_companyatlas_provider(
    name: str,
) -> Any:
    """Get address provider."""
    providers = get_providers(  # type: ignore[no-any-return]
        lib_name="companyatlas",
        attribute_search={"name": name},
        format="python",
    )
    if len(providers) > 1:
        raise ValueError(f"Expected 1 provider, got {len(providers)}")
    return providers[0]
    

def search_company(
    query: str,
    first: bool = False,
    providers: dict[str, Any] | None = None,
    json: str | Path | None = None,
    lib_name: str = "companyatlas",
    config: list[dict[str, Any]] | None = None,
    dir_path: str | Path | None = None,
    base_module: str | None = None,
    query_string: str | None = None,
    search_fields: list[str] | None = None,
    **kwargs: Any,
) -> Any:
    """Search company using providers."""
    if "additional_args" not in kwargs:
        kwargs["additional_args"] = {}
    kwargs["additional_args"]["query"] = query

    providers_args = {
        "command": "search_company",
        "json": json,
        "lib_name": lib_name,
        "config": config,
        "dir_path": dir_path,
        "base_module": base_module,
        "query_string": query_string,
        "search_fields": search_fields,
    }
    providers_args.update(kwargs)

    if first:
        return try_providers_first(**providers_args)
    return try_providers(**providers_args)


def search_company_by_code(
    code: str,
    first: bool = False,
    providers: dict[str, Any] | None = None,
    json: str | Path | None = None,
    lib_name: str = "companyatlas",
    config: list[dict[str, Any]] | None = None,
    dir_path: str | Path | None = None,
    base_module: str | None = None,
    query_string: str | None = None,
    search_fields: list[str] | None = None,
    **kwargs: Any,
) -> Any:
    """Search company by code using providers."""
    if "additional_args" not in kwargs:
        kwargs["additional_args"] = {}
    kwargs["additional_args"]["code"] = code
    providers_args = {
        "command": "search_company_by_code",
        "json": json,
        "lib_name": lib_name,
        "config": config,
        "dir_path": dir_path,
        "base_module": base_module,
        "query_string": query_string,
        "search_fields": search_fields,
    }
    providers_args.update(kwargs)

    if first:
        return try_providers_first(**providers_args)
    return try_providers(**providers_args)

def download_company_documents(
    code: str,
    first: bool = False,
    providers: dict[str, Any] | None = None,
    json: str | Path | None = None,
    lib_name: str = "companyatlas",
    config: list[dict[str, Any]] | None = None,
    dir_path: str | Path | None = None,
    base_module: str | None = None,
    query_string: str | None = None,
    search_fields: list[str] | None = None,
    **kwargs: Any,
) -> Any:
    """Download company documents using providers."""
    if "additional_args" not in kwargs:
        kwargs["additional_args"] = {}
    kwargs["additional_args"]["code"] = code
    providers_args = {
        "command": "download_company_documents",
        "json": json,
        "lib_name": lib_name,
        "config": config,
        "dir_path": dir_path,
        "base_module": base_module,
        "query_string": query_string,
        "search_fields": search_fields,
    }
    providers_args.update(kwargs)

    if first:
        return try_providers_first(**providers_args)
    return try_providers(**providers_args)

def get_company_events(
    code: str,
    first: bool = False,
    providers: dict[str, Any] | None = None,
    json: str | Path | None = None,
    lib_name: str = "companyatlas",
    config: list[dict[str, Any]] | None = None,
    dir_path: str | Path | None = None,
    base_module: str | None = None,
    query_string: str | None = None,
    search_fields: list[str] | None = None,
    **kwargs: Any,
) -> Any:
    """Get company events using providers."""
    if "additional_args" not in kwargs:
        kwargs["additional_args"] = {}
    kwargs["additional_args"]["code"] = code
    providers_args = {
        "command": "get_company_events",
        "json": json,
        "lib_name": lib_name,
        "config": config,
        "dir_path": dir_path,
        "base_module": base_module,
        "query_string": query_string,
        "search_fields": search_fields,
    }
    providers_args.update(kwargs)

    if first:
        return try_providers_first(**providers_args)
    return try_providers(**providers_args)