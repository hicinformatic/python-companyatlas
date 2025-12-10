"""Base backend class with generic functions for all country backends."""

import importlib
from abc import ABC, abstractmethod
from typing import Any

# Mapping ISO country codes to country names for flagpy
_COUNTRY_CODE_TO_NAME = {
    "FR": "France",
    "US": "United States",
    "GB": "United Kingdom",
    "DE": "Germany",
    "IT": "Italy",
    "ES": "Spain",
    "NL": "Netherlands",
    "BE": "Belgium",
    "CH": "Switzerland",
    "AT": "Austria",
    "SE": "Sweden",
    "NO": "Norway",
    "DK": "Denmark",
    "FI": "Finland",
    "PL": "Poland",
    "PT": "Portugal",
    "IE": "Ireland",
    "GR": "Greece",
    "CZ": "Czech Republic",
    "HU": "Hungary",
    "RO": "Romania",
    "BG": "Bulgaria",
    "HR": "Croatia",
    "SK": "Slovakia",
    "SI": "Slovenia",
    "LT": "Lithuania",
    "LV": "Latvia",
    "EE": "Estonia",
    "LU": "Luxembourg",
    "MT": "Malta",
    "CY": "Cyprus",
}


def get_country_flag_emoji(country_code: str) -> str:
    """Convert a country ISO code (2 letters) to flag emoji Unicode.

    Uses Regional Indicator Symbols (U+1F1E6 to U+1F1FF) to create
    flag emojis from ISO 3166-1 alpha-2 country codes.

    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., "FR", "US", "GB")

    Returns:
        Flag emoji Unicode string (e.g., "🇫🇷", "🇺🇸", "🇬🇧")
        Returns empty string if code is invalid

    Examples:
        >>> get_country_flag_emoji("FR")
        '🇫🇷'
        >>> get_country_flag_emoji("US")
        '🇺🇸'
        >>> get_country_flag_emoji("GB")
        '🇬🇧'
    """
    if not country_code or len(country_code) != 2:
        return ""

    country_code = country_code.upper()

    # Validate that both characters are letters
    if not country_code.isalpha():
        return ""

    # Use Regional Indicator Symbols (U+1F1E6 to U+1F1FF)
    # Each letter A-Z maps to U+1F1E6 + (ord(letter) - ord('A'))
    try:
        flag_emoji = "".join(chr(ord("🇦") + ord(letter) - ord("A")) for letter in country_code)
        return flag_emoji
    except (ValueError, TypeError):
        return ""


def get_country_flag_image_base64(country_code: str, size: tuple | None = None) -> str:
    """Get country flag as base64-encoded image using flagpy.

    Args:
        country_code: ISO 3166-1 alpha-2 country code (e.g., "FR", "US", "GB")
        size: Optional tuple (width, height) to resize the image. Default is (32, 16).

    Returns:
        Base64-encoded image data URL string (e.g., "data:image/png;base64,...")
        Returns empty string if code is invalid or flagpy is not available
    """
    if not country_code or len(country_code) != 2:
        return ""

    country_code = country_code.upper()

    # Get country name from mapping
    country_name = _COUNTRY_CODE_TO_NAME.get(country_code)
    if not country_name:
        return ""

    try:
        import base64
        from io import BytesIO

        import flagpy as fp

        # Get flag image
        img = fp.get_flag_img(country_name)

        # Resize if requested
        if size:
            img = img.resize(
                size, resample=img.__class__.LANCZOS if hasattr(img.__class__, "LANCZOS") else 1
            )
        else:
            # Default small size for admin display
            img = img.resize(
                (32, 16), resample=img.__class__.LANCZOS if hasattr(img.__class__, "LANCZOS") else 1
            )

        # Convert to base64
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except ImportError:
        # flagpy not installed, fallback to emoji
        return ""
    except Exception:
        # Any other error, return empty
        return ""


class BaseBackend(ABC):
    """Base class for all country-specific backends.

    This class provides the common interface that all backends must implement.
    Each country backend should inherit from this class and implement the
    abstract methods.
    """

    # Backend metadata
    name: str = "base"
    display_name: str | None = None
    description_text: str | None = None
    continent: str | None = None

    # Configuration
    config_keys: list[str] = []
    required_packages: list[str] = []

    # URLs
    status_url: str | None = None
    documentation_url: str | None = None
    site_url: str | None = None
    api_url: str | None = None

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize backend with configuration.

        Args:
            config: Configuration dictionary with API keys, endpoints, etc.
        """
        self._raw_config: dict[str, Any] = dict(config or {})
        self._config: dict[str, Any] = self._filter_config(self._raw_config)

    def _filter_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Extract the subset of config keys declared by the backend.

        Args:
            config: Raw configuration dictionary

        Returns:
            Filtered configuration dictionary containing only declared config_keys
        """
        if not self.config_keys:
            return dict(config)
        return {key: config[key] for key in self.config_keys if key in config}

    @property
    def config(self) -> dict[str, Any]:
        """Access configuration values.

        Returns:
            Filtered configuration dictionary
        """
        return self._config

    @property
    def label(self) -> str:
        """Human-friendly backend name.

        Returns:
            Display name or formatted name
        """
        if self.display_name:
            return self.display_name
        if self.name:
            return self.name.replace("_", " ").title()
        return self.__class__.__name__

    def configure(self, config: dict[str, Any], *, replace: bool = False) -> "BaseBackend":
        """Update backend configuration (filtered by config_keys).

        Args:
            config: Configuration dictionary to merge or replace
            replace: If True, replace existing config; otherwise merge

        Returns:
            Self for method chaining
        """
        if replace:
            self._raw_config = dict(config or {})
        else:
            self._raw_config.update(config or {})
        self._config = self._filter_config(self._raw_config)
        return self

    def check_package(self, package_name: str) -> bool:
        """Check if a required package is installed.

        Args:
            package_name: Name of the package to check

        Returns:
            True if the package can be imported, False otherwise
        """
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            # Try with hyphens replaced by underscores (e.g., sib-api-v3-sdk -> sib_api_v3_sdk)
            try:
                importlib.import_module(package_name.replace("-", "_"))
                return True
            except ImportError:
                return False

    def check_required_packages(self) -> dict[str, bool]:
        """Check all required packages and return their installation status.

        Returns:
            Dict mapping package names to their installation status
        """
        return {package: self.check_package(package) for package in self.required_packages}

    def check_config_keys(self, config: dict[str, Any] | None = None) -> dict[str, bool]:
        """Check if all config_keys are present in the provided configuration.

        Args:
            config: Configuration dict to check (defaults to self._raw_config)

        Returns:
            Dict mapping config key names to their presence status
        """
        if config is None:
            config = self._raw_config
        return {key: key in config for key in self.config_keys}

    def check_package_and_config(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Check both required packages and configuration keys.

        Args:
            config: Configuration dict to check (defaults to self._raw_config)

        Returns:
            Dict with 'packages' and 'config' keys containing their respective status dicts
        """
        return {
            "packages": self.check_required_packages(),
            "config": self.check_config_keys(config),
        }

    def get_status(self) -> dict[str, Any]:
        """Get backend status and availability information.

        Returns:
            Dictionary with status information including:
                - status: Current status ("working", "unavailable", "missing_config", etc.)
                - is_available: Boolean indicating if backend is operational
                - packages: Package installation status
                - config: Configuration status
                - warnings: List of warnings
        """
        check = self.check_package_and_config()
        packages = check.get("packages", {})
        config_status = check.get("config", {})

        missing_packages = [pkg for pkg, installed in packages.items() if not installed]
        missing_config = [key for key in self.config_keys if not config_status.get(key)]

        if missing_packages:
            status = "missing_packages"
        elif missing_config:
            status = "missing_config"
        else:
            status = "available"

        country_code = self.get_country_code()

        return {
            "status": status,
            "is_available": status == "available",
            "backend_name": self.name,
            "backend_display_name": self.label,
            "country_code": country_code,
            "country_flag": self.get_country_flag(),
            "country_flag_image": self.get_country_flag_image_base64(),
            "packages": packages,
            "config": config_status,
            "missing_packages": missing_packages,
            "missing_config": missing_config,
            "warnings": [],
            "documentation_url": self.documentation_url,
            "site_url": self.site_url,
            "status_url": self.status_url,
        }

    def validate(self) -> tuple[bool, str]:
        """Validate backend configuration.

        Returns:
            Tuple of (is_valid, error_message). Checks that required config keys
            are present and required packages are available.
        """
        check = self.check_package_and_config()
        packages = check.get("packages", {})
        config_status = check.get("config", {})

        missing_packages = [pkg for pkg, installed in packages.items() if not installed]
        missing_config = [key for key in self.config_keys if not config_status.get(key)]

        if missing_packages:
            return (
                False,
                f"Missing required packages: {', '.join(missing_packages)}",
            )

        if missing_config:
            return (
                False,
                f"Missing required configuration keys: {', '.join(missing_config)}",
            )

        return True, ""

    @abstractmethod
    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies/entities by name.

        This is a generic search that works with company names like "tour eiffel".

        Args:
            name: Company or entity name to search for
            **kwargs: Additional search parameters (country-specific)

        Returns:
            List of dictionaries containing company/entity information.
            Each dict should contain at minimum:
                - name: Company name
                - identifier: Primary identifier (SIREN, CRN, etc.)
                - country: ISO country code
        """
        pass

    @abstractmethod
    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company/entity by its registration code.

        This is a specific search using official registration codes like SIREN, RNA, etc.

        Args:
            code: Registration code (e.g., SIREN, RNA, CRN)
            code_type: Type of code (optional, backend may auto-detect)
            **kwargs: Additional search parameters

        Returns:
            Dictionary with company/entity information, or None if not found.
            Should contain:
                - name: Company name
                - identifier: The registration code
                - identifier_type: Type of identifier used
                - country: ISO country code
                - Additional country-specific fields
        """
        pass

    @abstractmethod
    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents/publications for a company/entity.

        This retrieves official publications like BODACC, BALO, etc.

        Args:
            identifier: Company identifier (SIREN, etc.)
            document_type: Type of document to retrieve (optional, may return all types)
            **kwargs: Additional filters (date range, document category, etc.)

        Returns:
            List of document dictionaries. Each dict should contain:
                - type: Document type (e.g., "bodacc", "balo")
                - title: Document title
                - date: Publication date (ISO format)
                - url: URL to access the document (if available)
                - Additional document-specific metadata
        """
        pass

    def get_country_code(self) -> str:
        """Get the ISO country code for this backend.

        Returns:
            ISO 3166-1 alpha-2 country code (e.g., "FR", "GB", "US")
        """
        return getattr(self, "country_code", "XX")

    def get_country_flag(self) -> str:
        """Get the country flag emoji for this backend.

        Returns:
            Country flag emoji Unicode string (e.g., "🇫🇷" for France)
            Returns empty string if country code is invalid
        """
        country_code = self.get_country_code()
        return get_country_flag_emoji(country_code)

    def get_country_flag_image_base64(self, size: tuple | None = None) -> str:
        """Get the country flag as base64-encoded image for this backend.

        Args:
            size: Optional tuple (width, height) to resize the image. Default is (32, 16).

        Returns:
            Base64-encoded image data URL string (e.g., "data:image/png;base64,...")
            Returns empty string if country code is invalid or flagpy is not available
        """
        country_code = self.get_country_code()
        return get_country_flag_image_base64(country_code, size=size)

    def get_continent(self) -> str | None:
        """Get the continent for this backend.

        Returns:
            Continent name (e.g., "europe", "americas", "asia", "africa", "oceania")
            or None if not specified
        """
        return getattr(self, "continent", None)

    def get_backend_name(self) -> str:
        """Get the name of this backend.

        Returns:
            Backend name identifier
        """
        return getattr(self, "backend_name", self.name)
