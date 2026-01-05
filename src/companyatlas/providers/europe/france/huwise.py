import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class HuwiseProvider(CompanyAtlasFranceProvider):
    name = "huwise"
    display_name = "Huwise"
    description = "Open data platform aggregating French public datasets"
    required_packages = ["requests"]
    config_keys = ["SIREN_DATASET_ID", "BASE_URL"]
    config_defaults = {
        "SIREN_DATASET_ID": "economicref-france-sirene-v3",
        "BASE_URL": "https://hub.huwise.com",
    }
    config_required = []
    documentation_url = "https://docs.huwise.com"
    site_url = "https://huwise.com"
    status_url = None
    provider_can_be_used = True

    fields_associations = {
        "siren": "siren",
        "rna": "identifiantassociationunitelegale",
        "siret": "siret",
        "denomination": ("denominationunitelegale", "denominationusuelleetablissement"),
        "since": "datecreationunitelegale",
        "legalform": "naturejuridiqueunitelegale",
        "ape": ("activiteprincipaleunitelegale", "activiteprincipaleetablissement"),
        "category": "categorieentreprise",
        "slice_effective": "trancheeffectifsunitelegale",
        "is_headquarter": "etablissementsiege",
        "address_line1": "adresseetablissement",
        "address_line2": "complementadresseetablissement",
        "address_line3": "complementadresse2etablissement",
        "city": "libellecommuneetablissement",
        "postal_code": "codepostaletablissement",
        "state": "departementetablissement",
        "region": "regionetablissement",
        "county": "libellecommuneetablissement",
        "country": "libellepaysetrangeretablissement",
        "country_code": "codepaysetrangeretablissement",
        "municipality": "libellecommuneetablissement",
        "neighbourhood": None,
        "latitude": "geolocetablissement.lat",
        "longitude": "geolocetablissement.lon",
    }

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def _call_api(self, query: str) -> list[dict[str, Any]]:
        if requests is None:
            return []
        dataset_id = self._get_config_or_env("SIREN_DATASET_ID", default="economicref-france-sirene-v3")
        base_url = self._get_config_or_env("BASE_URL", default="https://hub.huwise.com")
        url = f"{base_url}/api/explore/v2.1/catalog/datasets/{dataset_id}/records/"
        params = {"where": f"search({query})", "limit": 20, "lang": "fr", "offset": 0, "timezone": "Europe/Paris"}
        headers = {}
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception:
            return []

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        query_str = f'"{query}"'
        results = self._call_api(query_str)
        if raw:
            return results
        normalized = []
        for result in results:
            normalized_result = self.normalize(self.france_fields, result)
            normalized.append(normalized_result)
        return normalized

    def search_company_by_code(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        query_str = f'"{siren}"'
        results = self._call_api(query_str)
        result = results[0] if results else None
        if result is None:
            return None
        if raw:
            return result
        return self.normalize(self.france_fields, result)

