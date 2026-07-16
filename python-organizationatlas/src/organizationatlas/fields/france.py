"""France-specific OrganizationAtlas field definitions."""

FRANCE_FIELDS_DESCRIPTIONS = {
    "siren": "SIREN number (9 digits, French organization identifier)",
    "rna": "RNA number (W + 8 digits, French association identifier)",
    "siret": "SIRET number (14 digits, French establishment identifier)",
    "is_association": "Whether this is an association",
    "denomination": "Organization name or legal name",
    "since": "Organization creation date",
    "legalform": "Legal form code or description",
    "ape": "APE code (French activity code, NAF)",
    "category": "Organization category (e.g., PME, ETI, GE)",
    "slice_effective": "Employee count range code",
    "is_headquarter": "Whether this is the organization headquarters",
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

_SEARCH_FIELD_NAMES = {"ape", "legalform", "slice_effective", "category"}

FR_SEARCH_COMPANY_FIELDS = {
    key: value
    for key, value in FRANCE_FIELDS_DESCRIPTIONS.items()
    if key in _SEARCH_FIELD_NAMES
}
