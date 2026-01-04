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
    provider_can_be_used = False
    france_fields = list(FRANCE_FIELDS_DESCRIPTIONS.keys())
