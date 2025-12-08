"""Opendatasoft backend for French company data.

Opendatasoft is a data platform that provides access to various French
open data sources including company registries, public datasets, and
official publications.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime

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
    backend_name = "opendatasoft"
    display_name = "Opendatasoft"
    description_text = "Open data platform aggregating French public datasets"
    
    config_keys = ["api_key", "dataset_id"]
    required_packages = ["requests"]
    
    documentation_url = "https://help.opendatasoft.com/apis/ods-search-api"
    site_url = "https://data.opendatasoft.com"
    status_url = None
    api_url = "https://data.opendatasoft.com/api/explore/v2.1"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize Opendatasoft backend.

        Args:
            config: Configuration dictionary with:
                - api_key: Opendatasoft API key (optional, may be required for some datasets)
                - base_url: Base URL for Opendatasoft API
                - dataset_id: Default dataset ID to use
        """
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)
        self.dataset_id = self.config.get("dataset_id", "sirene@public")

    def search_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Search for companies by name using Opendatasoft datasets.

        Args:
            name: Company name to search for
            **kwargs: Additional parameters:
                - limit: Maximum number of results (default: 20, max: 100)
                - dataset_id: Specific dataset ID to search (default: SIRENE)
                - departement: Filter by French department code
                - code_naf: Filter by NAF code
                - active_only: Only return active companies (default: False)

        Returns:
            List of company dictionaries with:
                - siren: SIREN number
                - name: Company name (denomination)
                - legal_form: Legal form
                - status: Company status
                - address: Registered address
                - creation_date: Company creation date
                - activity: NAF code and activity description
        """
        if not name or not isinstance(name, str):
            return []

        limit = min(kwargs.get("limit", 20), 100)
        dataset_id = kwargs.get("dataset_id", self.dataset_id)
        departement = kwargs.get("departement")
        code_naf = kwargs.get("code_naf")
        active_only = kwargs.get("active_only", False)

        # TODO: Implement actual Opendatasoft API call
        # Example:
        # params = {
        #     "dataset": dataset_id,
        #     "q": name,
        #     "rows": limit,
        #     "refine.etatadministratifunitelegale": "A" if active_only else None,
        # }
        # if departement:
        #     params["refine.departementunitelegale"] = departement
        # if code_naf:
        #     params["refine.activiteprincipaleunitelegale"] = code_naf
        #
        # response = self._call_api("catalog/datasets", params=params)
        # return self._parse_search_results(response)

        return []

    def search_by_code(self, code: str, code_type: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """Search for a company by SIREN using Opendatasoft datasets.

        Args:
            code: SIREN number (9 digits)
            code_type: Should be "siren" or None (RNA not supported in default dataset)
            **kwargs: Additional parameters:
                - dataset_id: Specific dataset ID to search

        Returns:
            Dictionary with company information, or None if not found.
            Contains:
                - siren: SIREN number
                - name: Company name
                - legal_form: Legal form
                - status: Company status
                - address: Full registered address
                - creation_date: Company creation date
                - activity: NAF code and activity description
        """
        if code_type and code_type != "siren":
            raise ValueError(f"Opendatasoft default dataset only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        dataset_id = kwargs.get("dataset_id", self.dataset_id)

        # TODO: Implement actual Opendatasoft API call
        # Example:
        # params = {
        #     "dataset": dataset_id,
        #     "q": f"siren:{siren}",
        #     "rows": 1,
        # }
        # response = self._call_api("catalog/datasets", params=params)
        # if response and response.get("results"):
        #     return self._parse_company_data(response["results"][0])

        return None

    def get_documents(self, identifier: str, document_type: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
        """Get official documents/publications from Opendatasoft datasets.

        Opendatasoft provides access to various document datasets including:
        - BODACC publications
        - BALO publications
        - Other official publications

        Args:
            identifier: Entity identifier (SIREN)
            document_type: Type of document ("bodacc", "balo", or None for all)
            **kwargs: Additional filters:
                - date_from: Start date (ISO format or datetime)
                - date_to: End date (ISO format or datetime)
                - dataset_id: Specific dataset ID for documents
                - category: Document category

        Returns:
            List of document dictionaries with:
                - type: Document type
                - title: Document title
                - date: Publication date (ISO format)
                - url: URL to access the document
                - source: Document source dataset
                - Additional document-specific metadata
        """
        if not identifier:
            return []

        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        dataset_id = kwargs.get("dataset_id")
        category = kwargs.get("category")

        # Convert datetime to ISO string if needed
        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        documents = []

        # BODACC documents
        if not document_type or document_type == "bodacc":
            bodacc_dataset = dataset_id or "bodacc@public"
            bodacc_docs = self._get_documents_from_dataset(
                siren, bodacc_dataset, "bodacc", date_from, date_to, category
            )
            documents.extend(bodacc_docs)

        # BALO documents
        if not document_type or document_type == "balo":
            balo_dataset = dataset_id or "balo@public"
            balo_docs = self._get_documents_from_dataset(
                siren, balo_dataset, "balo", date_from, date_to, category
            )
            documents.extend(balo_docs)

        return documents

    def _get_documents_from_dataset(
        self,
        siren: str,
        dataset_id: str,
        document_type: str,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        category: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Get documents from a specific Opendatasoft dataset.

        Args:
            siren: SIREN number
            dataset_id: Dataset ID to query
            document_type: Type of document
            date_from: Start date filter
            date_to: End date filter
            category: Document category filter

        Returns:
            List of document dictionaries
        """
        # TODO: Implement actual Opendatasoft API call
        # params = {
        #     "dataset": dataset_id,
        #     "q": f"siren:{siren}",
        #     "rows": 100,
        # }
        # if date_from:
        #     params["refine.date_publication"] = f">={date_from}"
        # if date_to:
        #     params["refine.date_publication"] = f"<={date_to}"
        # if category:
        #     params["refine.categorie"] = category
        #
        # response = self._call_api("catalog/datasets", params=params)
        # return self._parse_documents(response, document_type)

        return []

    def list_available_datasets(self, **kwargs) -> List[Dict[str, Any]]:
        """List available datasets on Opendatasoft platform.

        Args:
            **kwargs: Additional parameters:
                - search: Search term for dataset names
                - country: Filter by country code

        Returns:
            List of dataset dictionaries with:
                - id: Dataset ID
                - name: Dataset name
                - description: Dataset description
                - source: Data source
                - last_update: Last update date
        """
        # TODO: Implement actual Opendatasoft API call
        # params = {}
        # if kwargs.get("search"):
        #     params["q"] = kwargs["search"]
        # if kwargs.get("country"):
        #     params["refine.country"] = kwargs["country"]
        #
        # response = self._call_api("catalog/datasets", params=params)
        # return self._parse_datasets(response)

        return []

    def _call_api(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """Make API call to Opendatasoft service.

        Args:
            endpoint: API endpoint path
            params: Query parameters

        Returns:
            API response as dictionary, or None on error
        """
        # TODO: Implement actual HTTP request
        # Should handle:
        # - API key authentication if required
        # - Rate limiting
        # - Error handling
        # - Response parsing
        return None

    def _parse_search_results(self, response: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parse Opendatasoft search API response.

        Args:
            response: Raw API response

        Returns:
            List of parsed company data dictionaries
        """
        # TODO: Implement response parsing
        return []

    def _parse_company_data(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """Parse Opendatasoft company data response.

        Args:
            response: Raw API response

        Returns:
            Parsed company data dictionary
        """
        # TODO: Implement response parsing
        return {}

    def _parse_documents(self, response: Dict[str, Any], document_type: str) -> List[Dict[str, Any]]:
        """Parse Opendatasoft documents API response.

        Args:
            response: Raw API response
            document_type: Type of documents being parsed

        Returns:
            List of parsed document dictionaries
        """
        # TODO: Implement response parsing
        return []

