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
    display_name = "SocieteInfo"
    description_text = "Enrichissement de données B2B et bases de données d'entreprises françaises"

    config_keys = ["api_key", "api_token"]
    required_packages = ["requests"]

    # SocieteInfo est un service d'enrichissement B2B
    # Principalement des données de sociétés enrichies, pas de documents/événements
    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.societeinfo.com/api"
    site_url = "https://www.societeinfo.com"
    status_url = None
    api_url = "https://api.societeinfo.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize SocieteInfo backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.api_token = self.config.get("api_token")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on SocieteInfo."""
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to SocieteInfo service."""
        return {}
