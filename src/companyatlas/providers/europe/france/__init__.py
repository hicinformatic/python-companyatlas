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
    geo_country_code = "FR"
    geo_country_name = "France"
    abstract = True
    france_fields = list(FRANCE_FIELDS_DESCRIPTIONS.keys())

    @staticmethod
    def is_siren(query: str) -> bool:
        """Check if query is a SIREN number (9 digits)."""
        if not query:
            return False
        siren_clean = re.sub(r"[\s-]", "", query)
        return bool(re.match(r"^\d{9}$", siren_clean))

    @staticmethod
    def is_rna(query: str) -> bool:
        """Check if query is an RNA number (W + 8 digits)."""
        if not query:
            return False
        rna_clean = re.sub(r"[\s-]", "", query.upper())
        return bool(re.match(r"^W\d{8}$", rna_clean))
