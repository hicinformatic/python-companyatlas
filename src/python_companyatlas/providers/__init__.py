"""Provider system for collecting company data by country.

Providers are organized by continent/country hierarchy:
    providers/
        europe/
            france/
                infogreffe.py
                pappers.py
            germany/
                handelsregister.py
        americas/
            usa/
                sec.py

Each provider implements BaseProvider interface.
"""

from typing import Protocol, Dict, Any, List, Optional


class BaseProvider(Protocol):
    """Base interface that all country providers must implement."""

    name: str
    country_code: str  # ISO 3166-1 alpha-2
    supported_data_types: List[str]  # ["addresses", "subsidiaries", "documents", "identifiers"]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize provider with configuration."""
        ...

    def lookup_by_identifier(self, identifier: str, identifier_type: str) -> Dict[str, Any]:
        """Look up company by identifier (SIREN, VAT, CRN, etc.).
        
        Args:
            identifier: Company identifier value
            identifier_type: Type of identifier (e.g., "siren", "vat", "crn")
            
        Returns:
            Dictionary with company data
        """
        ...

    def get_addresses(self, identifier: str) -> List[Dict[str, Any]]:
        """Get all company addresses (headquarters, branches, etc.)."""
        ...

    def get_subsidiaries(self, identifier: str) -> List[Dict[str, Any]]:
        """Get company subsidiaries and corporate structure."""
        ...

    def get_documents(self, identifier: str) -> List[Dict[str, Any]]:
        """Get official documents (registrations, reports, etc.)."""
        ...


__all__ = ["BaseProvider"]

