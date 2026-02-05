from typing import Any
import re

from .. import CompanyAtlasEuropeProvider

FRANCE_FIELDS_DESCRIPTIONS = {
    "siren": "SIREN number (9 digits, French company identifier)",
    "rna": "RNA number (W + 8 digits, French association identifier)",
    "siret": "SIRET number (14 digits, French establishment identifier)",
    "is_association": "Whether this is an association",
    "denomination": "Company name or legal name",
    "since": "Company creation date",
    "legalform": "Legal form code or description",
    "ape": "APE code (French activity code, NAF)",
    "category": "Company category (e.g., PME, ETI, GE)",
    "slice_effective": "Employee count range code",
    "is_headquarter": "Whether this is the company headquarters",
    "address_line1": "Street number and name",
    "address_line2": "Building, apartment, floor (optional)",
    "address_line3": "Additional address info (optional)",
    "city": "City name",
    "postal_code": "Postal code",
    "state": "Department code or name",
    "region": "Region code or name",
    "county": "County or administrative county",
    "country": "Country name",
    "country_code": "ISO country code (e.g., FR)",
    "municipality": "Municipality or commune",
    "neighbourhood": "Neighbourhood, quarter, or district",
    "latitude": "Latitude coordinate (float)",
    "longitude": "Longitude coordinate (float)",
}

class CompanyAtlasFranceProvider(CompanyAtlasEuropeProvider):
    geo_code = "FR"
    geo_country = "france"
    abstract = True
    france_fields = list(FRANCE_FIELDS_DESCRIPTIONS.keys())

    def is_siret(self, query: str) -> bool:
        """Check if query is a SIRET number (14 digits)."""
        if not query:
            return False
        siret_clean = re.sub(r"[\s-]", "", query)
        return bool(re.match(r"^\d{14}$", siret_clean))

    def is_siren(self, query: str) -> bool:
        """Check if query is a SIREN number (9 digits)."""
        if not query:
            return False
        siren_clean = re.sub(r"[\s-]", "", query)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def is_rna(self, query: str) -> bool:
        """Check if query is an RNA number (W + 8 digits)."""
        if not query:
            return False
        rna_clean = re.sub(r"[\s-]", "", query.upper())
        return bool(re.match(r"^W\d{8}$", rna_clean))

    def _validate_siret(self, siret: str) -> bool:
        siret_clean = re.sub(r"[\s-]", "", siret)
        return bool(re.match(r"^\d{14}$", siret_clean))

    def _format_siret(self, siret: str) -> str:
        siret_clean = re.sub(r"[\s-]", "", siret)
        return siret_clean[:14] if len(siret_clean) >= 14 else siret_clean

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def _validate_rna(self, rna: str) -> bool:
        rna_clean = re.sub(r"[\s-]", "", rna.upper())
        return bool(re.match(r"^W\d{8}$", rna_clean))

    def _format_rna(self, rna: str) -> str:
        rna_clean = re.sub(r"[\s-]", "", rna.upper())
        return rna_clean[:9] if len(rna_clean) >= 9 else rna_clean

    def _detect_code_type(self, code: str) -> str | None:
        """Detect the type of code (siren, siret, rna)."""
        if self.is_siret(code):
            return "siret"
        if self.is_siren(code):
            return "siren"
        if self.is_rna(code):
            return "rna"
        return None

    def get_normalize_source_field(self, data: dict[str, Any]) -> str | None:
        """Get the source field for a code (siren, siret, rna)."""
        cache = self._service_results_cache.get("search_company_by_reference", {})
        kwargs = cache.get("kwargs", {})
        code = kwargs.get("code", "")
        return self._detect_code_type(code)

