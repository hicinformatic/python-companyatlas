"""Societe.com backend.

This backend provides access to Societe.com which aggregates legal, financial,
and business information on French companies from INPI, INSEE, and RCS sources.
"""

from typing import Any

from .base import FrenchBaseBackend


class SocieteComBackend(FrenchBaseBackend):
    """Backend for Societe.com.

    Provides access to aggregated French company data from Societe.com.
    """

    name = "societecom"
    backend_name = "societecom"
    display_name = "Societe.com"
    description_text = (
        "Agrégateur d'informations légales, juridiques et financières "
        "sur les entreprises françaises"
    )

    config_keys = ["api_key", "api_secret"]
    required_packages = ["requests"]

    documentation_url = "https://www.societe.com/cgi-bin/api"
    site_url = "https://www.societe.com"
    status_url = None
    api_url = "https://api.societe.com"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize Societe.com backend.

        Args:
            config: Configuration dictionary with:
                - api_key: Societe.com API key (required)
                - api_secret: Societe.com API secret (if required)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.api_secret = self.config.get("api_secret")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name on Societe.com.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 10)
                - departement: Filter by department code
                - code_naf: Filter by NAF code

        Returns:
            List of company dictionaries with:
                - name: Company name
                - siren: SIREN number
                - address: Company address
                - activity: NAF code and activity description
        """
        kwargs.get("limit", 10)

        # TODO: Implement actual Societe.com API call
        # response = self._call_api("search", params={"q": name, "limit": limit})
        # return self._parse_search_response(response)

        return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN on Societe.com.

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
                - financial_data: Financial information
        """
        if code_type and code_type != "siren":
            return None

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual Societe.com API call
        # response = self._call_api(f"entreprise/{siren}")
        # return self._parse_entreprise_response(response)

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get documents from Societe.com.

        Args:
            identifier: SIREN number
            document_type: Type of document ("kbis", "financial", "legal", or None for all)
            **kwargs: Additional parameters

        Returns:
            List of document dictionaries
        """
        # TODO: Implement actual Societe.com documents API call
        return []

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        """Make API call to Societe.com service.

        Args:
            endpoint: API endpoint
            params: Query parameters

        Returns:
            API response as dictionary
        """
        # TODO: Implement actual API call
        return {}
