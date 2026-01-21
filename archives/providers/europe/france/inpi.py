"""INPI (Institut National de la Propriété Industrielle) backend.

This backend provides access to the French INPI database which contains
company registration data from the national business registry including
commercial, craft, agricultural, and independent businesses.
"""

from typing import Any

from .base import FrenchBaseBackend


class INPIBackend(FrenchBaseBackend):
    """Backend for INPI (Institut National de la Propriété Industrielle).

    Provides access to French company data from the official INPI registry.
    """

    name = "inpi"
    display_name = "INPI"
    description_text = (
        "Institut National de la Propriété Industrielle - Registre national des entreprises"
    )

    config_keys = ["API_KEY", "API_USERNAME", "API_PASSWORD", "BASE_URL"]
    config_defaults = {
        "BASE_URL": "https://api.inpi.fr",
    }
    required_packages = ["requests"]

    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    api_url = "https://api.inpi.fr"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize INPI backend."""
        super().__init__(config)
        self.api_key = self._get_config_or_env("API_KEY")
        self.username = self._get_config_or_env("API_USERNAME")
        self.password = self._get_config_or_env("API_PASSWORD")
        self.base_url = self._get_config_or_env("BASE_URL")

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in INPI database."""
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
        """Get official documents from INPI."""
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to INPI service."""
        return {}
