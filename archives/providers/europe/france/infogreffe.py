"""Infogreffe backend for French commercial court registry.

Infogreffe is the official French commercial court registry (Registre du Commerce
et des Sociétés) that provides access to official company registration data,
legal documents, and corporate information.
"""

from datetime import datetime
from typing import Any

from .base import FrenchBaseBackend


class InfogreffeBackend(FrenchBaseBackend):
    """Backend for Infogreffe commercial court registry.

    Infogreffe provides official data from the French commercial courts including:
    - Company registration information
    - Legal documents and publications
    - Corporate structure and changes
    - Official extracts (extraits K-bis)
    """

    name = "infogreffe"
    display_name = "Infogreffe"
    description_text = "French commercial court registry (Registre du Commerce et des Sociétés)"

    config_keys = ["api_key", "username", "password"]
    required_packages = ["requests"]

    can_fetch_documents = True
    can_fetch_events = True
    can_fetch_company_data = True

    request_cost = {
        "data": 5.0,
        "documents": 5.0,
        "events": 5.0,
    }

    documentation_url = "https://www.infogreffe.fr"
    site_url = "https://www.infogreffe.fr"
    status_url = None
    api_url = "https://api.infogreffe.fr"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Infogreffe backend."""
        super().__init__(config)
        self.api_key = self._get_config_or_env("api_key")
        self.username = self._get_config_or_env("username")
        self.password = self._get_config_or_env("password")
        self.base_url = self._get_config_or_env("base_url", default=self.api_url)

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN or RCS in Infogreffe registry."""
        if not code:
            return None

        if not code_type:
            # Check if it's an RCS format (e.g., "B 123 456 789")
            if " " in str(code) or len(str(code).replace(" ", "")) > 9:
                code_type = "rcs"
            else:
                code_type = "siren"

        if code_type == "siren":
            siren = self.format_siren(code)
            if not self.validate_siren(siren):
                return None
            return None

        elif code_type == "rcs":
            # RCS format: "B 123 456 789" or "B123456789"
            self._format_rcs(code)
            return None

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents from Infogreffe."""
        if not identifier:
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        kwargs.get("category")

        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        #     "type": document_type,
        #     "date_debut": date_from,
        #     "date_fin": date_to,
        #     "categorie": category,
        # })
        # return self._parse_documents(response)

        return []

    def get_events(
        self, identifier: str, event_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get events/changes for a company from Infogreffe."""
        if not identifier:
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        category = kwargs.get("category")

        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        #     "type": event_type,
        #     "date_debut": date_from,
        #     "date_fin": date_to,
        #     "categorie": category,
        # })
        # return self._parse_events(response)

        return []

    def get_extrait_kbis(self, siren: str, **kwargs) -> dict[str, Any] | None:
        """Get official Extrait K-bis for a company."""
        siren = self.format_siren(siren)
        if not self.validate_siren(siren):
            return None

        # return self._parse_kbis(response)

        return None

    def _format_rcs(self, rcs: str) -> str:
        """Format an RCS number."""
        if not rcs:
            return ""
        # Remove spaces and normalize
        rcs_clean = rcs.replace(" ", "").upper()
        return rcs_clean

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to Infogreffe service."""
        return None

    def _parse_search_results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse Infogreffe search API response."""
        return []

    def _parse_kbis(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse Extrait K-bis response."""
        return {}
