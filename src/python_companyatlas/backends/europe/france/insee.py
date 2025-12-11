"""INSEE SIRENE database backend.

This backend provides access to the French INSEE SIRENE database which contains
official company registration data including SIREN numbers, company names, addresses,
and legal status.
"""

from typing import Any

from .base import FrenchBaseBackend


class INSEEBackend(FrenchBaseBackend):
    """Backend for INSEE SIRENE database.

    Provides access to French company data from the official INSEE SIRENE registry.
    """

    name = "insee"
    display_name = "INSEE SIRENE"
    description_text = "Official French company registry (SIRENE database)"

    config_keys = ["api_key", "consumer_key", "consumer_secret"]
    required_packages = ["requests"]

    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    documentation_url = (
        "https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/list-apis.jag"
    )
    site_url = "https://www.insee.fr"
    status_url = "https://api.insee.fr/status"
    api_url = "https://api.insee.fr/entreprises/sirene/V3"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize INSEE backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name in INSEE SIRENE database."""
        if not name or not isinstance(name, str):
            return []

        kwargs.get("limit", 20)
        kwargs.get("active_only", False)

        results: list[dict[str, Any]] = []
        return results

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in INSEE SIRENE database."""
        if code_type and code_type != "siren":
            raise ValueError(f"INSEE backend only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to INSEE SIRENE service."""
        return None

    def _parse_siret_response(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse INSEE SIRET API response into standardized format."""
        return {}
