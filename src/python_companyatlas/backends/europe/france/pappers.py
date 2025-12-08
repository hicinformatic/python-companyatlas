"""Pappers backend for French company data.

Pappers is a French company data aggregator that provides comprehensive
information about companies including financial data, legal information,
and official documents.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

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
    backend_name = "pappers"
    display_name = "Pappers"
    description_text = "French company data aggregator with comprehensive business information"
    
    config_keys = ["api_key"]
    required_packages = ["requests"]
    
    documentation_url = "https://www.pappers.fr/api/documentation"
    site_url = "https://www.pappers.fr"
    status_url = "https://www.pappers.fr/api/status"
    api_url = "https://api.pappers.fr/v2"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Pappers backend.

        Args:
            config: Configuration dictionary with:
                - api_key: Pappers API key (required)
                - base_url: Base URL for Pappers API (defaults to official endpoint)
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get(
            "base_url",
            self.api_url
        )

    def search_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Search for companies by name using Pappers.

        Args:
            name: Company name to search for (e.g., "tour eiffel")
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 20, max: 100)
                - page: Page number for pagination (default: 1)
                - departement: Filter by French department code
                - code_naf: Filter by NAF code
                - forme_juridique: Filter by legal form

        Returns:
            List of company dictionaries with:
                - siren: SIREN number
                - name: Company name (denomination)
                - legal_form: Legal form
                - status: Company status
                - address: Registered address
                - creation_date: Company creation date
                - capital: Share capital
                - activity: NAF code and activity description
        """
        if not name or not isinstance(name, str):
            return []

        limit = min(kwargs.get("limit", 20), 100)
        page = kwargs.get("page", 1)
        departement = kwargs.get("departement")
        code_naf = kwargs.get("code_naf")
        forme_juridique = kwargs.get("forme_juridique")

        # TODO: Implement actual Pappers API call
        # Example:
        # params = {
        #     "q": name,
        #     "par_page": limit,
        #     "page": page,
        # }
        # if departement:
        #     params["departement"] = departement
        # if code_naf:
        #     params["code_naf"] = code_naf
        # if forme_juridique:
        #     params["forme_juridique"] = forme_juridique
        #
        # response = self._call_api("recherche", params=params)
        # return self._parse_search_results(response)

        return []

    def search_by_code(self, code: str, code_type: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """Search for a company by SIREN using Pappers.

        Args:
            code: SIREN number (9 digits)
            code_type: Should be "siren" or None (RNA not supported by Pappers)
            **kwargs: Additional parameters

        Returns:
            Dictionary with comprehensive company information, or None if not found.
            Contains:
                - siren: SIREN number
                - name: Company name
                - legal_form: Legal form
                - status: Company status
                - address: Full registered address
                - creation_date: Company creation date
                - capital: Share capital
                - activity: NAF code and activity description
                - financial_data: Financial statements if available
                - directors: List of directors
                - shareholders: Shareholder information
        """
        if code_type and code_type != "siren":
            raise ValueError(f"Pappers backend only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual Pappers API call
        # Example:
        # response = self._call_api(f"siren/{siren}")
        # if response:
        #     return self._parse_company_data(response)

        return None

    def get_documents(self, identifier: str, document_type: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
        """Get official documents for a company from Pappers.

        Pappers provides access to various documents including:
        - BODACC publications
        - Financial statements
        - Legal documents
        - Registration certificates

        Args:
            identifier: SIREN number
            document_type: Type of document ("bodacc", "financial", "legal", or None for all)
            **kwargs: Additional filters:
                - date_from: Start date (ISO format or datetime)
                - date_to: End date (ISO format or datetime)
                - category: Document category

        Returns:
            List of document dictionaries with:
                - type: Document type
                - title: Document title
                - date: Publication date (ISO format)
                - url: URL to access the document
                - source: Document source
                - Additional document-specific metadata
        """
        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        category = kwargs.get("category")

        # Convert datetime to ISO string if needed
        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        # TODO: Implement actual Pappers API call
        # Example:
        # params = {}
        # if date_from:
        #     params["date_debut"] = date_from
        # if date_to:
        #     params["date_fin"] = date_to
        # if document_type:
        #     params["type"] = document_type
        #
        # response = self._call_api(f"siren/{siren}/documents", params=params)
        # return self._parse_documents(response)

        return []

    def get_financial_data(self, siren: str, **kwargs) -> Optional[Dict[str, Any]]:
        """Get financial data for a company.

        Args:
            siren: SIREN number
            **kwargs: Additional parameters:
                - year: Specific year (default: latest available)

        Returns:
            Dictionary with financial data including:
                - revenue: Revenue
                - profit: Profit/loss
                - employees: Number of employees
                - year: Financial year
                - Additional financial metrics
        """
        siren = self.format_siren(siren)
        if not self.validate_siren(siren):
            return None

        # TODO: Implement actual Pappers API call
        # response = self._call_api(f"siren/{siren}/finances", params=kwargs)
        # return self._parse_financial_data(response)

        return None

    def _call_api(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make API call to Pappers service.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary, or None on error
        """
        # TODO: Implement actual HTTP request with authentication
        # Should handle:
        # - API key authentication in headers
        # - Rate limiting
        # - Error handling
        # - Response parsing
        return None

    def _parse_search_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Pappers search API response.

        Args:
            response: Raw API response

        Returns:
            List of parsed company data dictionaries
        """
        # TODO: Implement response parsing
        return []

    def _parse_company_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Pappers company data API response.

        Args:
            response: Raw API response

        Returns:
            Parsed company data dictionary
        """
        # TODO: Implement response parsing
        return {}
