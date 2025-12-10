"""Verif.com backend.

This backend provides access to Verif.com which offers company verification
and business information services for French companies.
"""

from typing import Any

from .base import FrenchBaseBackend


class VerifBackend(FrenchBaseBackend):
    """Backend for Verif.com.

    Provides access to company verification and business data from Verif.com.
    """

    name = "verif"
    backend_name = "verif"
    display_name = "Verif.com"
    description_text = "Vérification et informations sur les entreprises françaises"

    config_keys = ["api_key"]
    required_packages = ["requests"]

    documentation_url = "https://www.verif.com/api"
    site_url = "https://www.verif.com"
    status_url = None
    api_url = "https://api.verif.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Verif.com backend.

        Args:
            config: Configuration dictionary with:
                - api_key: Verif.com API key (required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on Verif.com.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)

        Returns:
            List of company dictionaries
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual Verif.com API call
        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on Verif.com.

        Args:
            code: SIREN number
            code_type: Should be "siren" or None
            **kwargs: Additional parameters

        Returns:
            Company dictionary with verification data
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual Verif.com API call
        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get documents from Verif.com.

        Args:
            identifier: SIREN number
            document_type: Type of document (optional)
            **kwargs: Additional parameters

        Returns:
            List of document dictionaries
        """
        # TODO: Implement actual Verif.com documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to Verif.com service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
