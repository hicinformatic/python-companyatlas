"""Base backend class with generic functions for all country backends."""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
import importlib


class BaseBackend(ABC):
    """Base class for all country-specific backends.

    This class provides the common interface that all backends must implement.
    Each country backend should inherit from this class and implement the
    abstract methods.
    """

    # Backend metadata
    name: str = "base"
    display_name: Optional[str] = None
    description_text: Optional[str] = None
    
    # Configuration
    config_keys: List[str] = []
    required_packages: List[str] = []
    
    # URLs
    status_url: Optional[str] = None
    documentation_url: Optional[str] = None
    site_url: Optional[str] = None
    api_url: Optional[str] = None

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize backend with configuration.

        Args:
            config: Configuration dictionary with API keys, endpoints, etc.
        """
        self._raw_config: Dict[str, Any] = dict(config or {})
        self._config: Dict[str, Any] = self._filter_config(self._raw_config)

    def _filter_config(self, config: Dict[str, Any]) -> Dict[str, Any]:
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
    def config(self) -> Dict[str, Any]:
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

    def configure(
        self, config: Dict[str, Any], *, replace: bool = False
    ) -> "BaseBackend":
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

    def check_required_packages(self) -> Dict[str, bool]:
        """Check all required packages and return their installation status.

        Returns:
            Dict mapping package names to their installation status
        """
        return {
            package: self.check_package(package) for package in self.required_packages
        }

    def check_config_keys(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, bool]:
        """Check if all config_keys are present in the provided configuration.

        Args:
            config: Configuration dict to check (defaults to self._raw_config)

        Returns:
            Dict mapping config key names to their presence status
        """
        if config is None:
            config = self._raw_config
        return {key: key in config for key in self.config_keys}

    def check_package_and_config(
        self, config: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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

    def get_status(self) -> Dict[str, Any]:
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

        missing_packages = [
            pkg for pkg, installed in packages.items() if not installed
        ]
        missing_config = [
            key for key in self.config_keys if not config_status.get(key)
        ]

        if missing_packages:
            status = "missing_packages"
        elif missing_config:
            status = "missing_config"
        else:
            status = "available"

        return {
            "status": status,
            "is_available": status == "available",
            "backend_name": self.name,
            "backend_display_name": self.label,
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

        missing_packages = [
            pkg for pkg, installed in packages.items() if not installed
        ]
        missing_config = [
            key for key in self.config_keys if not config_status.get(key)
        ]

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
    def search_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
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
    def search_by_code(self, code: str, code_type: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
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
    def get_documents(self, identifier: str, document_type: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
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
        return getattr(self, 'country_code', 'XX')

    def get_backend_name(self) -> str:
        """Get the name of this backend.

        Returns:
            Backend name identifier
        """
        return getattr(self, 'backend_name', self.name)

