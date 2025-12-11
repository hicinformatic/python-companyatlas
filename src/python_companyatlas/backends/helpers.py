"""Helper functions for discovering and managing backends."""

from typing import Any

from . import (
    BODACCBackend,
    CCIBackend,
    EntDataGouvBackend,
    EspaceDocsBackend,
    InfogreffeBackend,
    INPIBackend,
    INSEEBackend,
    OpendatasoftBackend,
    PappersBackend,
    PharowBackend,
    SocieteComBackend,
    SocieteDataBackend,
    SocieteInfoBackend,
    VerifBackend,
)
from .base import BaseBackend

# List of all backend classes (excluding base classes)
_ALL_BACKEND_CLASSES = [
    BODACCBackend,
    INSEEBackend,
    EntDataGouvBackend,
    PappersBackend,
    InfogreffeBackend,
    OpendatasoftBackend,
    INPIBackend,
    SocieteComBackend,
    VerifBackend,
    SocieteInfoBackend,
    CCIBackend,
    SocieteDataBackend,
    PharowBackend,
    EspaceDocsBackend,
]


def get_all_backend_classes() -> list[type[BaseBackend]]:
    """Get all available backend classes.

    Returns:
        List of backend class types (not instances)
    """
    return list(_ALL_BACKEND_CLASSES)


def get_all_backends(config: dict[str, Any] | None = None) -> list[BaseBackend]:
    """Get instances of all available backends.

    Args:
        config: Optional configuration dictionary to pass to all backends

    Returns:
        List of backend instances
    """
    return [backend_class(config=config) for backend_class in _ALL_BACKEND_CLASSES]


def get_backends(
    config: dict[str, Any] | None = None,
    *,
    continent: str | None = None,
    country_code: str | None = None,
    can_fetch_documents: bool | None = None,
    can_fetch_events: bool | None = None,
    can_fetch_company_data: bool | None = None,
    search: str | None = None,
) -> list[dict[str, Any]]:
    """Get status information for all backends with optional filtering.

    Args:
        config: Optional configuration dictionary to pass to all backends
        continent: Filter by continent name (e.g., "europe")
        country_code: Filter by ISO country code (e.g., "FR")
        can_fetch_documents: Filter by documents capability (True/False)
        can_fetch_events: Filter by events capability (True/False)
        can_fetch_company_data: Filter by company data capability (True/False)
        search: Search in name or display_name (case-insensitive)

    Returns:
        List of dictionaries containing backend status information.
        Each dict includes:
            - name: Backend identifier
            - display_name: Human-readable name
            - continent: Continent name
            - country_code: ISO country code
            - status: Current status
            - is_available: Boolean indicating if backend is operational
            - can_fetch_documents: Whether backend can fetch documents
            - can_fetch_events: Whether backend can fetch events
            - can_fetch_company_data: Whether backend can fetch company data
            - missing_packages: List of missing packages
            - missing_config: List of missing config keys
            - documentation_url: URL to documentation
            - site_url: URL to backend website
    """
    backends = get_all_backends(config=config)
    statuses = []

    for backend in backends:
        status = backend.get_status()
        status["continent"] = backend.get_continent()
        status["country_code"] = backend.get_country_code()

        if continent and status.get("continent", "").lower() != continent.lower():
            continue

        if country_code and status.get("country_code", "").upper() != country_code.upper():
            continue

        if can_fetch_documents is not None and status.get("can_fetch_documents") != can_fetch_documents:
            continue

        if can_fetch_events is not None and status.get("can_fetch_events") != can_fetch_events:
            continue

        if can_fetch_company_data is not None and status.get("can_fetch_company_data") != can_fetch_company_data:
            continue

        if search:
            search_lower = search.lower()
            name = status.get("name", "").lower()
            display_name = status.get("display_name", "").lower()
            if search_lower not in name and search_lower not in display_name:
                continue

        statuses.append(status)

    return statuses


def get_backends_sorted(
    config: dict[str, Any] | None = None,
    sort_by: str = "continent",
    **filters,
) -> dict[str, Any]:
    """Get all backends sorted by continent and country.

    Args:
        config: Optional configuration dictionary to pass to all backends
        sort_by: Sort key - "continent" (default) or "country"
        **filters: Additional filters (continent, country_code, can_fetch_*, search)

    Returns:
        Dictionary organized by continent/country hierarchy:
        {
            "europe": {
                "FR": [
                    {
                        "name": "insee",
                        "display_name": "INSEE SIRENE",
                        "status": "available",
                        ...
                    },
                    ...
                ]
            },
            ...
        }
    """
    statuses = get_backends(config=config, **filters)

    if sort_by == "continent":
        continent_result: dict[str, dict[str, list[dict[str, Any]]]] = {}

        for status in statuses:
            continent = status.get("continent") or "unknown"
            country_code = status.get("country_code") or "XX"

            if continent not in continent_result:
                continent_result[continent] = {}

            if country_code not in continent_result[continent]:
                continent_result[continent][country_code] = []

            continent_result[continent][country_code].append(status)

        return continent_result

    elif sort_by == "country":
        country_result: dict[str, list[dict[str, Any]]] = {}

        for status in statuses:
            country_code = status.get("country_code") or "XX"

            if country_code not in country_result:
                country_result[country_code] = []

            country_result[country_code].append(status)

        return country_result

    else:
        raise ValueError(f"Invalid sort_by value: {sort_by}. Use 'continent' or 'country'")


def get_backends_by_continent(
    continent: str, config: dict[str, Any] | None = None, **filters
) -> list[dict[str, Any]]:
    """Get all backends for a specific continent.

    Args:
        continent: Continent name (e.g., "europe", "americas")
        config: Optional configuration dictionary to pass to all backends
        **filters: Additional filters (can_fetch_*, search)

    Returns:
        List of backend status dictionaries for the specified continent
    """
    return get_backends(config=config, continent=continent, **filters)


def get_backends_by_country(
    country_code: str, config: dict[str, Any] | None = None, **filters
) -> list[dict[str, Any]]:
    """Get all backends for a specific country.

    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., "FR", "GB", "US")
        config: Optional configuration dictionary to pass to all backends
        **filters: Additional filters (can_fetch_*, search)

    Returns:
        List of backend status dictionaries for the specified country
    """
    return get_backends(config=config, country_code=country_code, **filters)


def search_backends(
    query: str,
    config: dict[str, Any] | None = None,
    **filters,
) -> list[dict[str, Any]]:
    """Search backends by name or display_name.

    Args:
        query: Search query (searches in name and display_name)
        config: Optional configuration dictionary to pass to all backends
        **filters: Additional filters (continent, country_code, can_fetch_*)

    Returns:
        List of backend status dictionaries matching the search query
    """
    return get_backends(config=config, search=query, **filters)


__all__ = [
    "get_all_backend_classes",
    "get_all_backends",
    "get_backends",
    "get_backends_sorted",
    "get_backends_by_continent",
    "get_backends_by_country",
    "search_backends",
]
