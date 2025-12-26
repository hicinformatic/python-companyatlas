"""Societe.com backend.

This backend provides access to Societe.com which aggregates legal, financial,
and business information on French companies from INPI, INSEE, and RCS sources.
"""

from typing import Any

from .base import FrenchBaseBackend


class SocieteComBackend(FrenchBaseBackend):
    """Backend for Societe.com.

    Provides access to aggregated French company data from Societe.com.
    """

    name = "societecom"
    display_name = "Societe.com"
    description_text = (
        "Agrégateur d'informations légales, juridiques et financières "
        "sur les entreprises françaises"
    )

    config_keys = ["api_key", "api_secret"]
    required_packages = ["requests"]

    # Societe.com est un agrégateur qui peut fournir des documents
    # mais pas nécessairement des événements structurés
    can_fetch_documents = True
    can_fetch_events = False
    can_fetch_company_data = True

    request_cost = {
        "data": 5.0,
        "documents": 5.0,
        "events": "free",
    }

    documentation_url = "https://www.societe.com/cgi-bin/api"
    site_url = "https://www.societe.com"
    status_url = None
    api_url = "https://api.societe.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Societe.com backend."""
        super().__init__(config)
        self.api_key = self._get_config_or_env("api_key")
        self.api_secret = self._get_config_or_env("api_secret")
        self.base_url = self._get_config_or_env("base_url", default=self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on Societe.com."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # return self._parse_entreprise_response(response)

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get documents from Societe.com."""
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to Societe.com service."""
        return {}
