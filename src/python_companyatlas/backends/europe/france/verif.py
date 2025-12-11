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
    display_name = "Verif.com"
    description_text = "Vérification et informations sur les entreprises françaises"

    config_keys = ["api_key"]
    required_packages = ["requests"]

    # Verif.com est un service de vérification d'entreprises
    # Principalement des données de sociétés, pas de documents/événements
    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.verif.com/api"
    site_url = "https://www.verif.com"
    status_url = None
    api_url = "https://api.verif.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Verif.com backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on Verif.com."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to Verif.com service."""
        return {}
