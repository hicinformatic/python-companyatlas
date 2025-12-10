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
    backend_name = "insee"
    display_name = "INSEE SIRENE"
    description_text = "Official French company registry (SIRENE database)"

    config_keys = ["api_key", "consumer_key", "consumer_secret"]
    required_packages = ["requests"]

    documentation_url = (
        "https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/list-apis.jag"
    )
    site_url = "https://www.insee.fr"
    status_url = "https://api.insee.fr/status"
    api_url = "https://api.insee.fr/entreprises/sirene/V3"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize INSEE backend.

        Args:
            config: Configuration dictionary with:
                - api_key: INSEE API key (optional, may be required for some endpoints)
                - base_url: Base URL for INSEE API (defaults to official endpoint)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name in INSEE SIRENE database.

        Args:
            name: Company name to search for (e.g., "tour eiffel")
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 20)
                - active_only: Only return active companies (default: False)

        Returns:
            List of company dictionaries with:
                - siren: SIREN number
                - name: Company name (denomination)
                - legal_form: Legal form (SARL, SA, etc.)
                - status: Company status
                - address: Registered address
                - creation_date: Company creation date
        """
        if not name or not isinstance(name, str):
            return []

        kwargs.get("limit", 20)
        kwargs.get("active_only", False)

        # TODO: Implement actual INSEE API call
        # This is a placeholder structure
        results: list[dict[str, Any]] = []

        # Example structure for actual implementation:
        # response = self._call_api("siret", params={
        #     "q": f"denominationUniteLegale:{name}",
        #     "nombre": limit,
        #     "etatAdministratifUniteLegale": "A" if active_only else None
        # })

        return results

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in INSEE SIRENE database.

        Args:
            code: SIREN number (9 digits)
            code_type: Should be "siren" or None (RNA not supported by INSEE)
            **kwargs: Additional parameters

        Returns:
            Dictionary with company information, or None if not found.
            Contains:
                - siren: SIREN number
                - name: Company name (denomination)
                - legal_form: Legal form
                - status: Company status
                - address: Full registered address
                - creation_date: Company creation date
                - activity: NAF code and activity description
                - capital: Share capital (if available)
        """
        if code_type and code_type != "siren":
            raise ValueError(f"INSEE backend only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual INSEE API call
        # Example:
        # response = self._call_api(f"siret/{siren}")
        # if response:
        #     return self._parse_siret_response(response)

        return None

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents for a company.

        Note: INSEE SIRENE database itself doesn't provide BODACC/BALO documents,
        but this method can return company registration data as documents.

        Args:
            identifier: SIREN number
            document_type: Document type filter (not used for INSEE)
            **kwargs: Additional filters

        Returns:
            List of document dictionaries (registration data)
        """
        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        # INSEE doesn't provide BODACC/BALO, but we can return registration info
        company_data = self.search_by_code(siren)
        if not company_data:
            return []

        # Return registration data as a document
        documents = []
        if company_data.get("creation_date"):
            documents.append(
                {
                    "type": "registration",
                    "title": "Inscription au registre du commerce",
                    "date": company_data["creation_date"],
                    "source": "INSEE SIRENE",
                    "identifier": siren,
                }
            )

        return documents

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to INSEE SIRENE service.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary, or None on error
        """
        # TODO: Implement actual HTTP request with authentication
        # Should handle:
        # - OAuth2 authentication if api_key is provided
        # - Rate limiting
        # - Error handling
        # - Response parsing
        return None

    def _parse_siret_response(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse INSEE SIRET API response into standardized format.

        Args:
            response: Raw API response

        Returns:
            Parsed company data dictionary
        """
        # TODO: Implement response parsing
        return {}
