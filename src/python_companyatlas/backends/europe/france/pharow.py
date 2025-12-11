"""Pharow backend.

This backend provides access to Pharow which aggregates various B2B data sources
to provide comprehensive company information and data enrichment services.
"""

from typing import Any

from .base import FrenchBaseBackend


class PharowBackend(FrenchBaseBackend):
    """Backend for Pharow.

    Provides access to aggregated B2B data from Pharow.
    """

    name = "pharow"
    display_name = "Pharow"
    description_text = (
        "Agrégation de sources de données B2B pour enrichir les informations sur les entreprises"
    )

    config_keys = ["api_key", "api_secret"]
    required_packages = ["requests"]

    # Pharow est un agrégateur B2B pour l'enrichissement de données
    # Principalement des données de sociétés enrichies, pas de documents/événements
    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.pharow.com/api"
    site_url = "https://www.pharow.com"
    status_url = None
    api_url = "https://api.pharow.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Pharow backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.api_secret = self.config.get("api_secret")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on Pharow."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to Pharow service."""
        return {}
