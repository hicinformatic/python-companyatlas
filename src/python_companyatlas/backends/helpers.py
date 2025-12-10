"""Helper functions for discovering and managing backends."""

from typing import Any

from . import (
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


def get_backends(config: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    """Get status information for all backends.

    Args:
        config: Optional configuration dictionary to pass to all backends

    Returns:
        List of dictionaries containing backend status information.
        Each dict includes:
            - backend_name: Backend identifier
            - backend_display_name: Human-readable name
            - continent: Continent name
            - country_code: ISO country code
            - status: Current status
            - is_available: Boolean indicating if backend is operational
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
        statuses.append(status)

    return statuses


def get_backends_sorted(
    config: dict[str, Any] | None = None,
    sort_by: str = "continent",
) -> dict[str, Any]:
    """Get all backends sorted by continent and country.

    Args:
        config: Optional configuration dictionary to pass to all backends
        sort_by: Sort key - "continent" (default) or "country"

    Returns:
        Dictionary organized by continent/country hierarchy:
        {
            "europe": {
                "FR": [
                    {
                        "backend_name": "insee",
                        "backend_display_name": "INSEE SIRENE",
                        "status": "available",
                        ...
                    },
                    ...
                ]
            },
            ...
        }
    """
    statuses = get_backends(config=config)

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
    continent: str, config: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Get all backends for a specific continent.

    Args:
        continent: Continent name (e.g., "europe", "americas")
        config: Optional configuration dictionary to pass to all backends

    Returns:
        List of backend status dictionaries for the specified continent
    """
    statuses = get_backends(config=config)
    return [
        status for status in statuses if status.get("continent", "").lower() == continent.lower()
    ]


def get_backends_by_country(
    country_code: str, config: dict[str, Any] | None = None
) -> list[dict[str, Any]]:
    """Get all backends for a specific country.

    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., "FR", "GB", "US")
        config: Optional configuration dictionary to pass to all backends

    Returns:
        List of backend status dictionaries for the specified country
    """
    statuses = get_backends(config=config)
    return [
        status
        for status in statuses
        if status.get("country_code", "").upper() == country_code.upper()
    ]


__all__ = [
    "get_all_backend_classes",
    "get_all_backends",
    "get_backends",
    "get_backends_sorted",
    "get_backends_by_continent",
    "get_backends_by_country",
]
