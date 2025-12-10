"""EspaceDocs backend.

This backend provides access to EspaceDocs which offers instant access to
official information on French companies including legal documents, financial
statements, and business data.
"""

from typing import Any

from .base import FrenchBaseBackend


class EspaceDocsBackend(FrenchBaseBackend):
    """Backend for EspaceDocs.

    Provides access to official company documents and data from EspaceDocs.
    """

    name = "espacedocs"
    backend_name = "espacedocs"
    display_name = "EspaceDocs"
    description_text = (
        "Accès instantané aux informations officielles sur toutes les entreprises françaises"
    )

    config_keys = ["api_key"]
    required_packages = ["requests"]

    documentation_url = "https://www.espacedocs.net/api"
    site_url = "https://www.espacedocs.net"
    status_url = None
    api_url = "https://api.espacedocs.net"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize EspaceDocs backend.

        Args:
            config: Configuration dictionary with:
                - api_key: EspaceDocs API key (required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on EspaceDocs.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)

        Returns:
            List of company dictionaries
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual EspaceDocs API call
        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on EspaceDocs.

        Args:
            code: SIREN number
            code_type: Should be "siren" or None
            **kwargs: Additional parameters

        Returns:
            Company dictionary with official documents and data
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual EspaceDocs API call
        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents from EspaceDocs.

        Args:
            identifier: SIREN number
            document_type: Type of document ("kbis", "financial", "legal", or None for all)
            **kwargs: Additional parameters:
                - date_from: Start date (ISO format)
                - date_to: End date (ISO format)

        Returns:
            List of document dictionaries with:
                - type: Document type (kbis, bilan, etc.)
                - title: Document title
                - date: Publication date
                - url: Download URL
        """
        # TODO: Implement actual EspaceDocs documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to EspaceDocs service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
