import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class OpendatasoftProvider(CompanyAtlasFranceProvider):
    name = "opendatasoft"
    display_name = "Opendatasoft"
    description = "Open data platform aggregating French public datasets"
    required_packages = ["requests"]
    config_keys = ["OPENDATASOFT_API_KEY", "OPENDATASOFT_DATASET_ID"]
    documentation_url = "https://help.opendatasoft.com/apis/ods-search-api"
    site_url = "https://data.opendatasoft.com"
    status_url = None
    provider_can_be_used = True

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def _call_api(self, query: str) -> list[dict[str, Any]]:
        if requests is None:
            return []
        dataset_id = self._get_config_or_env("OPENDATASOFT_DATASET_ID", default="economicref-france-sirene-v3@public")
        api_key = self._get_config_or_env("OPENDATASOFT_API_KEY")
        url = f"https://data.opendatasoft.com/api/explore/v2.1/catalog/datasets/{dataset_id}/records"
        params = {"q": query, "limit": 20}
        headers = {}
        if api_key:
            headers["apikey"] = api_key
        try:
            response = requests.get(url, params=params, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("results", [])
        except Exception:
            return []

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        query_str = f'nom_complet:"{query}"'
        return self._call_api(query_str)

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        query_str = f"siren:{siren}"
        results = self._call_api(query_str)
        return results[0] if results else None

