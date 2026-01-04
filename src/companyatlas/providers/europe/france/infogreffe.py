import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class InfogreffeProvider(CompanyAtlasFranceProvider):
    name = "infogreffe"
    display_name = "Infogreffe"
    description = "French commercial court registry (Registre du Commerce et des Sociétés)"
    required_packages = ["requests"]
    config_keys = ["INFOGREFFE_API_KEY", "INFOGREFFE_USERNAME", "INFOGREFFE_PASSWORD"]
    documentation_url = "https://www.infogreffe.fr"
    site_url = "https://www.infogreffe.fr"
    status_url = None
    provider_can_be_used = True

    fields_associations = {
        "siren": "siren",
        "rna": None,
        "siret": "siret",
        "denomination": "denomination",
        "since": "date_creation",
        "legalform": "forme_juridique",
        "ape": "activite_principale",
        "category": None,
        "slice_effective": None,
        "is_headquarter": "est_siege",
        "address_line1": "adresse.ligne1",
        "address_line2": "adresse.ligne2",
        "address_line3": "adresse.ligne3",
        "city": "adresse.ville",
        "postal_code": "adresse.code_postal",
        "state": "adresse.departement",
        "region": "adresse.region",
        "county": "adresse.ville",
        "country": "adresse.pays",
        "country_code": "adresse.code_pays",
        "municipality": "adresse.ville",
        "neighbourhood": None,
        "latitude": "adresse.latitude",
        "longitude": "adresse.longitude",
    }

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        return []

    def search_company_by_code(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN or RCS."""
        if not code:
            return None
        code_clean = re.sub(r"[\s-]", "", code)
        if re.match(r"^\d{9}$", code_clean):
            siren = self._format_siren(code)
            if not self._validate_siren(siren):
                return None
            return None
        return None

