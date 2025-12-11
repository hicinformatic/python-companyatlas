"""data.gouv.fr entities backend.

This backend provides access to French entity data from data.gouv.fr,
including associations (RNA), companies, and official publications.
"""

from datetime import datetime
from typing import Any

from .base import FrenchBaseBackend


class EntDataGouvBackend(FrenchBaseBackend):
    """Backend for data.gouv.fr entities.

    Provides access to French entity data from the official data.gouv.fr platform,
    including associations (RNA) and company data.
    """

    name = "entdatagouv"
    display_name = "data.gouv.fr"
    description_text = "French open data platform for public entities and datasets"

    config_keys = ["dataset_id"]
    required_packages = ["requests"]

    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = "https://www.data.gouv.fr/api"
    site_url = "https://www.data.gouv.fr"
    status_url = None
    api_url = "https://www.data.gouv.fr/api/1"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize data.gouv.fr backend."""
        super().__init__(config)
        self.dataset_id = self.config.get("dataset_id")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for entities by name on data.gouv.fr."""
        if not name or not isinstance(name, str):
            return []

        kwargs.get("limit", 20)
        kwargs.get("entity_type")

        results: list[dict[str, Any]] = []
        return results

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for an entity by SIREN or RNA on data.gouv.fr."""
        if not code:
            return None

        if not code_type:
            code_type = self.detect_identifier_type(code)

        if code_type == "siren":
            siren = self.format_siren(code)
            if not self.validate_siren(siren):
                return None
            return None

        elif code_type == "rna":
            rna = self.format_rna(code)
            if not self.validate_rna(rna):
                return None
            return None

        return None

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to data.gouv.fr."""
        return None
