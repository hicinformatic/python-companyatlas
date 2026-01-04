import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class PappersProvider(CompanyAtlasFranceProvider):
    name = "pappers"
    display_name = "Pappers"
    description = "French company data aggregator with comprehensive business information"
    required_packages = ["requests"]
    config_keys = ["PAPPERS_API_KEY"]
    documentation_url = "https://www.pappers.fr/api/documentation"
    site_url = "https://www.pappers.fr"
    status_url = "https://www.pappers.fr/api/status"
    provider_can_be_used = True

    fields_associations = {
        "siren": "siren",
        "rna": None,
        "siret": "siege.siret",
        "denomination": ("nom", "denomination"),
        "since": "date_creation",
        "legalform": "forme_juridique",
        "ape": "activite_principale",
        "category": "categorie_entreprise",
        "slice_effective": "tranche_effectif",
        "is_headquarter": "siege.est_siege",
        "address_line1": "siege.adresse",
        "address_line2": "siege.complement_adresse",
        "address_line3": None,
        "city": "siege.ville",
        "postal_code": "siege.code_postal",
        "state": "siege.departement",
        "region": "siege.region",
        "county": "siege.ville",
        "country": "siege.pays",
        "country_code": "siege.code_pays",
        "municipality": "siege.ville",
        "neighbourhood": None,
        "latitude": "siege.latitude",
        "longitude": "siege.longitude",
    }

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def _call_api(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        if requests is None:
            return None
        api_key = self._get_config_or_env("PAPPERS_API_KEY")
        if not api_key:
            return None
        url = f"https://api.pappers.fr/v2{endpoint}"
        headers = {"X-Api-Key": api_key}
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        params = {"q": query, "curseur": "*", "par_page": 20}
        data = self._call_api("/recherche", params)
        if data:
            results = data.get("resultats", [])
            if raw:
                return results
            normalized = []
            for result in results:
                normalized_result = self.normalize(self.france_fields, result)
                normalized.append(normalized_result)
            return normalized
        return []

    def search_company_by_code(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        data = self._call_api(f"/entreprise", {"siren": siren})
        if data is None:
            return None
        if raw:
            return data
        return self.normalize(self.france_fields, data)

