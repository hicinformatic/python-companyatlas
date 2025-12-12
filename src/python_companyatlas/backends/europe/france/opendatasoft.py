"""Opendatasoft backend for French company data.

Opendatasoft is a data platform that provides access to various French
open data sources including company registries, public datasets, and
official publications.
"""

from datetime import datetime
from typing import Any

from .base import FrenchBaseBackend


class OpendatasoftBackend(FrenchBaseBackend):
    """Backend for Opendatasoft platform.

    Opendatasoft aggregates data from multiple French open data sources:
    - INSEE SIRENE datasets
    - BODACC publications
    - BALO publications
    - Regional and local datasets
    - Public entity registries
    """

    name = "opendatasoft"
    display_name = "Opendatasoft"
    description_text = "Open data platform aggregating French public datasets"

    config_keys = ["api_key", "dataset_id"]
    required_packages = ["requests"]

    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    request_cost = {
        "data": "free",
        "documents": "free",
        "events": "free",
    }

    documentation_url = "https://help.opendatasoft.com/apis/ods-search-api"
    site_url = "https://data.opendatasoft.com"
    status_url = None
    api_url = "https://data.opendatasoft.com/api/explore/v2.1"
    default_dataset_id = "economicref-france-sirene-v3@public"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Opendatasoft backend."""
        super().__init__(config)
        self.api_key = self._get_config_or_env("api_key")
        self.dataset_id = self._get_config_or_env("dataset_id", default=self.default_dataset_id)
        self.base_url = self._get_config_or_env("base_url", default=self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on Opendatasoft."""
        if not name or not isinstance(name, str):
            return []

        min(kwargs.get("limit", 20), 100)
        kwargs.get("dataset_id", self.dataset_id)
        kwargs.get("departement")
        kwargs.get("code_naf")
        kwargs.get("active_only", False)

        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN using Opendatasoft datasets."""
        if code_type and code_type != "siren":
            raise ValueError(
                f"Opendatasoft default dataset only supports SIREN codes, not {code_type}"
            )

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        kwargs.get("dataset_id", self.dataset_id)


        return []

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to Opendatasoft service."""
        return None

    def _parse_search_results(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse Opendatasoft search API response."""
        return []

    def _parse_company_data(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse Opendatasoft company data response."""
        return {}

    def _parse_documents(
        self, response: dict[str, Any], document_type: str
    ) -> list[dict[str, Any]]:
        """Parse Opendatasoft documents API response."""
        return []
