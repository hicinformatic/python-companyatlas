"""SocieteData backend.

This backend provides access to SocieteData which offers legal, financial,
and strategic data on over 12 million French companies.
"""

from typing import Any

from .base import FrenchBaseBackend


class SocieteDataBackend(FrenchBaseBackend):
    """Backend for SocieteData.

    Provides access to comprehensive company data from SocieteData.
    """

    name = "societedata"
    backend_name = "societedata"
    display_name = "SocieteData"
    description_text = (
        "Données légales, financières et stratégiques sur plus de "
        "12 millions d'entreprises françaises"
    )

    config_keys = ["api_key"]
    required_packages = ["requests"]

    documentation_url = "https://www.societedata.net/api"
    site_url = "https://www.societedata.net"
    status_url = None
    api_url = "https://api.societedata.net"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize SocieteData backend.

        Args:
            config: Configuration dictionary with:
                - api_key: SocieteData API key (required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on SocieteData.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)

        Returns:
            List of company dictionaries with legal, financial, and strategic data
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual SocieteData API call
        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on SocieteData.

        Args:
            code: SIREN number
            code_type: Should be "siren" or None
            **kwargs: Additional parameters

        Returns:
            Company dictionary with comprehensive data
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual SocieteData API call
        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get documents from SocieteData.

        Args:
            identifier: SIREN number
            document_type: Type of document ("financial", "legal", "strategic", or None for all)
            **kwargs: Additional parameters

        Returns:
            List of document dictionaries
        """
        # TODO: Implement actual SocieteData documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to SocieteData service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
