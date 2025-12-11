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
    display_name = "EspaceDocs"
    description_text = (
        "Accès instantané aux informations officielles sur toutes les entreprises françaises"
    )

    config_keys = ["api_key"]
    required_packages = ["requests"]

    can_fetch_documents = True
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.espacedocs.net/api"
    site_url = "https://www.espacedocs.net"
    status_url = None
    api_url = "https://api.espacedocs.net"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize EspaceDocs backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on EspaceDocs."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents from EspaceDocs."""
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to EspaceDocs service."""
        return {}
