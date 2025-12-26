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

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        params = {"q": query, "curseur": "*", "par_page": 20}
        data = self._call_api("/recherche", params)
        if data:
            return data.get("resultats", [])
        return []

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        data = self._call_api(f"/entreprise", {"siren": siren})
        return data

