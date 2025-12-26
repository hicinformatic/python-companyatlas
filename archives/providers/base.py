"""Base backend class with generic functions for all country backends."""

import importlib
import os
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

    if not country_code.isalpha():
        return ""

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

    country_name = _COUNTRY_CODE_TO_NAME.get(country_code)
    if not country_name:
        return ""

    try:
        import base64
        from io import BytesIO

        import flagpy as fp

        img = fp.get_flag_img(country_name)

        if size:
            img = img.resize(
                size, resample=img.__class__.LANCZOS if hasattr(img.__class__, "LANCZOS") else 1
            )
        else:
            img = img.resize(
                (32, 16), resample=img.__class__.LANCZOS if hasattr(img.__class__, "LANCZOS") else 1
            )

        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"
    except ImportError:
        return ""
    except Exception:
        return ""


class BaseBackend(ABC):
    """Base class for all country-specific backends.

    This class provides the common interface that all backends must implement.
    Each country backend should inherit from this class and implement the
    abstract methods.
    """

    name: str = "base"
    display_name: str | None = None
    description_text: str | None = None
    continent: str | None = None

    config_keys: list[str] = []
    required_packages: list[str] = []

    status_url: str | None = None
    documentation_url: str | None = None
    site_url: str | None = None
    api_url: str | None = None

    can_fetch_documents: bool = False
    can_fetch_events: bool = False
    can_fetch_company_data: bool = True

    request_cost: dict[str, str | float] = {
        "data": "free",
        "documents": "free",
        "events": "free",
    }

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize backend with configuration."""
        self._raw_config: dict[str, Any] = dict(config or {})
        self._config: dict[str, Any] = self._filter_config(self._raw_config)

    def _filter_config(self, config: dict[str, Any]) -> dict[str, Any]:
        """Extract the subset of config keys declared by the backend."""
        if not self.config_keys:
            return dict(config)
        return {key: config[key] for key in self.config_keys if key in config}

    @property
    def config(self) -> dict[str, Any]:
        """Access configuration values."""
        return self._config

    @property
    def label(self) -> str:
        """Human-friendly backend name."""
        if self.display_name:
            return self.display_name
        if self.name:
            return self.name.replace("_", " ").title()
        return self.__class__.__name__

    def configure(self, config: dict[str, Any], *, replace: bool = False) -> "BaseBackend":
        """Update backend configuration."""
        if replace:
            self._raw_config = dict(config or {})
        else:
            self._raw_config.update(config or {})
        self._config = self._filter_config(self._raw_config)
        return self

    def _get_config_or_env(self, key: str, default: Any = None) -> Any:
        """Get config value from config dict or environment variable.

        Priority order:
        1. Config dict (highest priority)
        2. Environment variable
        3. Default parameter (lowest priority)

        Environment variable name format: COMPANYATLAS_{BACKEND_NAME}_{KEY}
        (all uppercase, underscores).

        Args:
            key: Configuration key name
            default: Default value if not found in config or env

        Returns:
            Configuration value from config, env, or default
        """
        value = self.config.get(key)
        if value is not None:
            return value

        backend_name = self.name.upper().replace("-", "_")
        env_key = f"COMPANYATLAS_{backend_name}_{key.upper()}"
        return os.getenv(env_key, default)

    def check_package(self, package_name: str) -> bool:
        """Check if a required package is installed."""
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            try:
                importlib.import_module(package_name.replace("-", "_"))
                return True
            except ImportError:
                return False

    def check_required_packages(self) -> dict[str, bool]:
        """Check all required packages and return their installation status."""
        return {package: self.check_package(package) for package in self.required_packages}

    def check_config_keys(self, config: dict[str, Any] | None = None) -> dict[str, bool]:
        """Check if all config_keys are present in the provided configuration or environment."""
        if config is None:
            config = self._raw_config
        result = {}
        for key in self.config_keys:
            if key in config and config[key] is not None:
                result[key] = True
            else:
                backend_name = self.name.upper().replace("-", "_")
                env_key = f"COMPANYATLAS_{backend_name}_{key.upper()}"
                result[key] = os.getenv(env_key) is not None
        return result

    def check_package_and_config(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Check both required packages and configuration keys."""
        if config is None:
            config = self._raw_config
        return {key: key in config for key in self.config_keys}

    def check_package_and_config(self, config: dict[str, Any] | None = None) -> dict[str, Any]:
        """Check both required packages and configuration keys."""
        return {
            "packages": self.check_required_packages(),
            "config": self.check_config_keys(config),
        }

    def get_status(self) -> dict[str, Any]:
        """Get backend status and availability information."""
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
            "name": self.name,
            "display_name": self.label,
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
            "can_fetch_documents": self.can_fetch_documents,
            "can_fetch_events": self.can_fetch_events,
            "can_fetch_company_data": self.can_fetch_company_data,
            "request_cost": self.request_cost,
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
        """Search for companies/entities by name."""
        pass

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company/entity by its registration code."""
        raise NotImplementedError(
            f"Backend {self.name} does not support fetching company data"
        )

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents/publications for a company/entity."""
        raise NotImplementedError(
            f"Backend {self.name} does not support fetching documents"
        )

    def get_events(
        self, identifier: str, event_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get events/changes for a company/entity."""
        raise NotImplementedError(
            f"Backend {self.name} does not support fetching events"
        )

    def fetch_data(
        self, identifier: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Fetch company/entity data by identifier."""
        if not self.can_fetch_company_data:
            raise NotImplementedError(
                f"Backend {self.name} does not support fetching company data"
            )
        return self.search_by_code(identifier, code_type=code_type, **kwargs)

    def fetch_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Fetch documents for a company/entity by identifier."""
        if not self.can_fetch_documents:
            raise NotImplementedError(
                f"Backend {self.name} does not support fetching documents"
            )
        return self.get_documents(identifier, document_type=document_type, **kwargs)

    def fetch_events(
        self, identifier: str, event_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Fetch events/changes for a company/entity by identifier."""
        if not self.can_fetch_events:
            raise NotImplementedError(
                f"Backend {self.name} does not support fetching events"
            )
        return self.get_events(identifier, event_type=event_type, **kwargs)

    def get_country_code(self) -> str:
        """Get the ISO country code for this backend."""
        return getattr(self, "country_code", "XX")

    def get_country_flag(self) -> str:
        """Get the country flag emoji for this backend."""
        country_code = self.get_country_code()
        return get_country_flag_emoji(country_code)

    def get_country_flag_image_base64(self, size: tuple | None = None) -> str:
        """Get the country flag as base64-encoded image for this backend."""
        country_code = self.get_country_code()
        return get_country_flag_image_base64(country_code, size=size)

    def get_continent(self) -> str | None:
        """Get the continent for this backend."""
        return getattr(self, "continent", None)

