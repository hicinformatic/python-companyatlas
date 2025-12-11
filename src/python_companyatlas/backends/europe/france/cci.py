"""CCI (Chambres de Commerce et d'Industrie) Annuaire backend.

This backend provides access to the French CCI directory which lists
companies registered with the Chambers of Commerce and Industry.
"""

from typing import Any

from .base import FrenchBaseBackend


class CCIBackend(FrenchBaseBackend):
    """Backend for CCI Annuaire des Entreprises.

    Provides access to French company data from the CCI directory.
    """

    name = "cci"
    display_name = "CCI Annuaire"
    description_text = "Annuaire des Entreprises de France - Chambres de Commerce et d'Industrie"

    config_keys = ["api_key"]
    required_packages = ["requests"]

    # CCI Annuaire est un annuaire d'entreprises
    # Principalement des données de sociétés, pas de documents/événements
    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.cci.fr/web/annuaire-entreprises"
    site_url = "https://www.cci.fr"
    status_url = None
    api_url = "https://api.cci.fr"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize CCI backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in CCI directory."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to CCI service."""
        return {}
