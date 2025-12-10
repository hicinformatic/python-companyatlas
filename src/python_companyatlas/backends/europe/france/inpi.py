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
    backend_name = "inpi"
    display_name = "INPI"
    description_text = (
        "Institut National de la Propriété Industrielle - Registre national des entreprises"
    )

    config_keys = ["api_key", "username", "password"]
    required_packages = ["requests"]

    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    api_url = "https://api.inpi.fr"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize INPI backend.

        Args:
            config: Configuration dictionary with:
                - api_key: INPI API key (optional)
                - username: Username for authentication (if required)
                - password: Password for authentication (if required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.username = self.config.get("username")
        self.password = self.config.get("password")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name in INPI database.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)
                - code_naf: Filter by NAF code

        Returns:
            List of company dictionaries with:
                - name: Company name
                - siren: SIREN number
                - siret: SIRET number
                - address: Company address
                - activity: NAF code and activity description
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual INPI API call
        # response = self._call_api("search", params={"q": name, "limit": limit})
        # return self._parse_search_response(response)

        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in INPI database.

        Args:
            code: SIREN number
            code_type: Should be "siren" or None
            **kwargs: Additional parameters

        Returns:
            Company dictionary with:
                - name: Company name
                - siren: SIREN number
                - siret: SIRET number
                - address: Company address
                - activity: NAF code and activity description
                - legal_form: Legal form
                - registration_date: Registration date
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual INPI API call
        # response = self._call_api(f"entreprise/{siren}")
        # return self._parse_entreprise_response(response)

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents from INPI.

        Args:
            identifier: SIREN number
            document_type: Type of document ("kbis", "financial", "legal", or None for all)
            **kwargs: Additional parameters:
                - date_from: Start date (ISO format)
                - date_to: End date (ISO format)

        Returns:
            List of document dictionaries with:
                - type: Document type
                - title: Document title
                - date: Publication date
                - url: Download URL
        """
        # TODO: Implement actual INPI documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to INPI service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
