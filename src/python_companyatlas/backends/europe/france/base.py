"""Base backend for French company data.

This module provides French-specific base functions and common utilities
for all French backends (INSEE, data.gouv.fr, etc.).
"""

import re
from typing import Any

from ...base import BaseBackend


class FrenchBaseBackend(BaseBackend):
    """Base class for French company data backends.

    Provides common functionality for French backends including:
    - SIREN validation and formatting
    - RNA validation and formatting
    - Common search patterns
    """

    continent = "europe"
    country_code = "FR"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize French backend."""
        super().__init__(config)

    def validate_siren(self, siren: str) -> bool:
        """Validate a SIREN number."""
        if not siren:
            return False

        siren_clean = re.sub(r"[\s-]", "", str(siren))

        if not re.match(r"^\d{9}$", siren_clean):
            return False

        return self._luhn_check(siren_clean)

    def format_siren(self, siren: str) -> str:
        """Format a SIREN number."""
        if not siren:
            return ""
        siren_clean = re.sub(r"[\s-]", "", str(siren))
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def validate_rna(self, rna: str) -> bool:
        """Validate an RNA number."""
        if not rna:
            return False

        rna_clean = re.sub(r"[\s-]", "", str(rna).upper())

        return bool(re.match(r"^W\d{8}$", rna_clean))

    def format_rna(self, rna: str) -> str:
        """Format an RNA number."""
        if not rna:
            return ""
        rna_clean = re.sub(r"[\s-]", "", str(rna).upper())
        if rna_clean.startswith("W"):
            return rna_clean[:9] if len(rna_clean) >= 9 else rna_clean
        digits = re.sub(r"[^\d]", "", rna_clean)
        if len(digits) == 8:
            return f"W{digits}"
        return rna_clean

    def detect_identifier_type(self, identifier: str) -> str | None:
        """Detect the type of French identifier (SIREN or RNA)."""
        identifier_clean = re.sub(r"[\s-]", "", str(identifier).upper())

        if self.validate_siren(identifier_clean):
            return "siren"
        if self.validate_rna(identifier_clean):
            return "rna"

        return None

    def _luhn_check(self, number: str) -> bool:
        """Perform Luhn algorithm check for SIREN validation."""
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

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies/entities by name."""
        raise NotImplementedError("Subclasses must implement search_by_name")

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company/entity by its registration code (SIREN or RNA)."""
        raise NotImplementedError("Subclasses must implement search_by_code")

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get official documents/publications for a company/entity."""
        raise NotImplementedError("Subclasses must implement get_documents")
