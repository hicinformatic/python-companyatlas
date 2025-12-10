"""SocieteInfo backend.

This backend provides access to SocieteInfo which offers B2B data enrichment
services and company databases for French businesses.
"""

from typing import Any

from .base import FrenchBaseBackend


class SocieteInfoBackend(FrenchBaseBackend):
    """Backend for SocieteInfo.

    Provides access to B2B data enrichment and company information from SocieteInfo.
    """

    name = "societeinfo"
    backend_name = "societeinfo"
    display_name = "SocieteInfo"
    description_text = "Enrichissement de données B2B et bases de données d'entreprises françaises"

    config_keys = ["api_key", "api_token"]
    required_packages = ["requests"]

    documentation_url = "https://www.societeinfo.com/api"
    site_url = "https://www.societeinfo.com"
    status_url = None
    api_url = "https://api.societeinfo.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize SocieteInfo backend.

        Args:
            config: Configuration dictionary with:
                - api_key: SocieteInfo API key (required)
                - api_token: API token (if required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.api_token = self.config.get("api_token")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on SocieteInfo.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)

        Returns:
            List of company dictionaries with enriched B2B data
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual SocieteInfo API call
        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on SocieteInfo.

        Args:
            code: SIREN number
            code_type: Should be "siren" or None
            **kwargs: Additional parameters

        Returns:
            Company dictionary with enriched B2B data
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual SocieteInfo API call
        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get documents from SocieteInfo.

        Args:
            identifier: SIREN number
            document_type: Type of document (optional)
            **kwargs: Additional parameters

        Returns:
            List of document dictionaries
        """
        # TODO: Implement actual SocieteInfo documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to SocieteInfo service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
