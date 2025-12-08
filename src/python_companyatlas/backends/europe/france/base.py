"""Base backend for French company data.

This module provides French-specific base functions and common utilities
for all French backends (INSEE, data.gouv.fr, etc.).
"""

from typing import Dict, Any, List, Optional
import re

from ...base import BaseBackend


class FrenchBaseBackend(BaseBackend):
    """Base class for French company data backends.

    Provides common functionality for French backends including:
    - SIREN validation and formatting
    - RNA validation and formatting
    - Common search patterns
    """

    country_code = "FR"

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """Initialize French backend.

        Args:
            config: Configuration dictionary
        """
        super().__init__(config)

    def validate_siren(self, siren: str) -> bool:
        """Validate a SIREN number.

        SIREN is a 9-digit number used to identify French companies.

        Args:
            siren: SIREN number to validate

        Returns:
            True if valid, False otherwise
        """
        if not siren:
            return False

        # Remove spaces and hyphens
        siren_clean = re.sub(r'[\s-]', '', str(siren))

        # Must be exactly 9 digits
        if not re.match(r'^\d{9}$', siren_clean):
            return False

        # Luhn algorithm validation
        return self._luhn_check(siren_clean)

    def format_siren(self, siren: str) -> str:
        """Format a SIREN number (remove spaces/hyphens, ensure 9 digits).

        Args:
            siren: SIREN number to format

        Returns:
            Formatted SIREN (9 digits)
        """
        if not siren:
            return ""
        siren_clean = re.sub(r'[\s-]', '', str(siren))
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def validate_rna(self, rna: str) -> bool:
        """Validate an RNA (Répertoire National des Associations) number.

        RNA is a 9-character identifier (W + 8 digits) for French associations.

        Args:
            rna: RNA number to validate

        Returns:
            True if valid, False otherwise
        """
        if not rna:
            return False

        # Remove spaces and hyphens
        rna_clean = re.sub(r'[\s-]', '', str(rna).upper())

        # Must be W followed by 8 digits
        return bool(re.match(r'^W\d{8}$', rna_clean))

    def format_rna(self, rna: str) -> str:
        """Format an RNA number (W + 8 digits).

        Args:
            rna: RNA number to format

        Returns:
            Formatted RNA (W + 8 digits)
        """
        if not rna:
            return ""
        rna_clean = re.sub(r'[\s-]', '', str(rna).upper())
        if rna_clean.startswith('W'):
            return rna_clean[:9] if len(rna_clean) >= 9 else rna_clean
        # If missing W prefix, add it
        digits = re.sub(r'[^\d]', '', rna_clean)
        if len(digits) == 8:
            return f"W{digits}"
        return rna_clean

    def detect_identifier_type(self, identifier: str) -> Optional[str]:
        """Detect the type of French identifier (SIREN or RNA).

        Args:
            identifier: Identifier to analyze

        Returns:
            "siren", "rna", or None if unknown
        """
        identifier_clean = re.sub(r'[\s-]', '', str(identifier).upper())

        if self.validate_siren(identifier_clean):
            return "siren"
        if self.validate_rna(identifier_clean):
            return "rna"

        return None

    def _luhn_check(self, number: str) -> bool:
        """Perform Luhn algorithm check for SIREN validation.

        Args:
            number: 9-digit number to check

        Returns:
            True if passes Luhn check
        """
        if len(number) != 9:
            return False

        total = 0
        for i, digit in enumerate(reversed(number)):
            n = int(digit)
            if i % 2 == 1:
                n *= 2
                if n > 9:
                    n -= 9
            total += n

        return total % 10 == 0

    def search_by_name(self, name: str, **kwargs) -> List[Dict[str, Any]]:
        """Search for companies/entities by name.

        This is a generic search that works with company names like "tour eiffel".

        Args:
            name: Company or entity name to search for
            **kwargs: Additional search parameters

        Returns:
            List of dictionaries containing company/entity information
        """
        raise NotImplementedError("Subclasses must implement search_by_name")

    def search_by_code(self, code: str, code_type: Optional[str] = None, **kwargs) -> Optional[Dict[str, Any]]:
        """Search for a company/entity by its registration code (SIREN or RNA).

        Args:
            code: Registration code (SIREN or RNA)
            code_type: Type of code ("siren" or "rna"), auto-detected if None
            **kwargs: Additional search parameters

        Returns:
            Dictionary with company/entity information, or None if not found
        """
        raise NotImplementedError("Subclasses must implement search_by_code")

    def get_documents(self, identifier: str, document_type: Optional[str] = None, **kwargs) -> List[Dict[str, Any]]:
        """Get official documents/publications for a company/entity.

        Retrieves publications like BODACC, BALO, etc.

        Args:
            identifier: Company identifier (SIREN)
            document_type: Type of document ("bodacc", "balo", or None for all)
            **kwargs: Additional filters (date_from, date_to, category, etc.)

        Returns:
            List of document dictionaries
        """
        raise NotImplementedError("Subclasses must implement get_documents")

