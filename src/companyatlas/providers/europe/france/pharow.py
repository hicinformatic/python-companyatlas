import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class PharowProvider(CompanyAtlasFranceProvider):
    name = "pharow"
    display_name = "Pharow"
    description = "Agrégation de sources de données B2B pour enrichir les informations sur les entreprises"
    required_packages = ["requests"]
    config_keys = ["PHAROW_API_KEY", "PHAROW_API_SECRET"]
    documentation_url = "https://www.pharow.com/api"
    site_url = "https://www.pharow.com"
    status_url = None
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
        api_key = self._get_config_or_env("PHAROW_API_KEY")
        api_secret = self._get_config_or_env("PHAROW_API_SECRET")
        if not api_key or not api_secret:
            return None
        url = f"https://api.pharow.com{endpoint}"
        headers = {"X-Api-Key": api_key, "X-Api-Secret": api_secret}
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        return []

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        data = self._call_api(f"/company/{siren}")
        return data

