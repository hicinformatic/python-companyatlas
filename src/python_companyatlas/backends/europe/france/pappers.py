"""Pappers backend for French company data.

Pappers is a French company data aggregator that provides comprehensive
information about companies including financial data, legal information,
and official documents.
"""

from datetime import datetime
from typing import Any

from .base import FrenchBaseBackend


class PappersBackend(FrenchBaseBackend):
    """Backend for Pappers API.

    Pappers aggregates data from multiple French sources including:
    - INSEE SIRENE
    - Infogreffe
    - BODACC
    - Financial statements
    - Legal documents
    """

    name = "pappers"
    display_name = "Pappers"
    description_text = "French company data aggregator with comprehensive business information"

    config_keys = ["api_key"]
    required_packages = ["requests"]

    can_fetch_documents = True
    can_fetch_events = True
    can_fetch_company_data = True

    documentation_url = "https://www.pappers.fr/api/documentation"
    site_url = "https://www.pappers.fr"
    status_url = "https://www.pappers.fr/api/status"
    api_url = "https://api.pappers.fr/v2"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Pappers backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on Pappers."""
        if not name or not isinstance(name, str):
            return []

        min(kwargs.get("limit", 20), 100)
        kwargs.get("page", 1)
        kwargs.get("departement")
        kwargs.get("code_naf")
        kwargs.get("forme_juridique")

        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN using Pappers."""
        if code_type and code_type != "siren":
            raise ValueError(f"Pappers backend only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None


        return []

    def get_events(
        self, identifier: str, event_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get events/changes for a company from Pappers."""
        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        category = kwargs.get("category")

        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        #     params["date_debut"] = date_from
        #     params["date_fin"] = date_to
        #     params["type"] = event_type
        #     params["categorie"] = category
        #
        # return self._parse_events(response)

        return []

    def get_financial_data(self, siren: str, **kwargs) -> dict[str, Any] | None:
        """Get financial data for a company."""
        siren = self.format_siren(siren)
        if not self.validate_siren(siren):
            return None

        # return self._parse_financial_data(response)

        return None

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to Pappers service."""
        return None

    def _parse_search_results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse Pappers search API response."""
        return []

    def _parse_company_data(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse Pappers company data API response."""
        return {}
