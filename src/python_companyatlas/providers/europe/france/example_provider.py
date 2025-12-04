"""Example French provider - demonstrates the structure.

This is a placeholder showing how to implement a provider.
"""

from typing import Dict, Any, List, Optional


class ExampleFrenchProvider:
    """Example provider for French company data.
    
    This demonstrates the structure that real providers should follow.
    Replace with actual implementation (InfogreffeProvider, PappersProvider, etc.)
    """

    name = "example_french"
    country_code = "FR"
    supported_data_types = ["addresses", "subsidiaries", "documents", "identifiers"]

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize provider with configuration.
        
        Args:
            config: Configuration dict with API keys, endpoints, etc.
        """
        self.config = config or {}
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", "https://api.example.fr")

    def lookup_by_identifier(
        self, identifier: str, identifier_type: str = "siren"
    ) -> Dict[str, Any]:
        """Look up company by identifier.
        
        Args:
            identifier: Company identifier (SIREN, VAT, etc.)
            identifier_type: Type of identifier (default: "siren")
            
        Returns:
            Dictionary with company data
            
        Raises:
            ValueError: If identifier is invalid
        """
        if not identifier:
            raise ValueError("Identifier cannot be empty")

        # TODO: Implement actual API call
        return {
            "identifier": identifier,
            "identifier_type": identifier_type,
            "name": f"Company {identifier}",
            "country": "FR",
            "status": "pending",
        }

    def get_addresses(self, identifier: str) -> List[Dict[str, Any]]:
        """Get all company addresses.
        
        Args:
            identifier: Company identifier (SIREN)
            
        Returns:
            List of address dictionaries with:
                - type: "headquarters", "branch", "registered_office"
                - street, city, postal_code, country
                - coordinates: latitude, longitude
        """
        # TODO: Implement actual API call
        return [
            {
                "type": "headquarters",
                "street": "123 Rue de la Paix",
                "city": "Paris",
                "postal_code": "75001",
                "country": "FR",
                "coordinates": {"latitude": 48.8566, "longitude": 2.3522},
            }
        ]

    def get_subsidiaries(self, identifier: str) -> List[Dict[str, Any]]:
        """Get company subsidiaries.
        
        Args:
            identifier: Parent company identifier (SIREN)
            
        Returns:
            List of subsidiary dictionaries with:
                - identifier: Subsidiary identifier
                - name: Subsidiary name
                - ownership_percentage: Ownership percentage
                - country: Country code
        """
        # TODO: Implement actual API call
        return []

    def get_documents(self, identifier: str) -> List[Dict[str, Any]]:
        """Get official documents.
        
        Args:
            identifier: Company identifier (SIREN)
            
        Returns:
            List of document dictionaries with:
                - type: "registration", "financial_statement", "legal_notice"
                - title: Document title
                - date: Publication date
                - url: Download URL
        """
        # TODO: Implement actual API call
        return []


__all__ = ["ExampleFrenchProvider"]

