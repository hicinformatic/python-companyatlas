import re
from typing import Any
from urllib.parse import quote

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class EntdatagouvProvider(CompanyAtlasFranceProvider):
    name = "entdatagouv"
    display_name = "data.gouv.fr"
    description = "French open data platform for public entities and datasets"
    required_packages = ["requests"]
    config_keys = []
    documentation_url = "https://www.data.gouv.fr/api"
    site_url = "https://www.data.gouv.fr"
    status_url = None
    provider_can_be_used = True

    def _detect_code_type(self, code: str) -> str | None:
        code_clean = re.sub(r"[\s-]", "", code)
        if re.match(r"^\d{9}$", code_clean):
            return "siren"
        if re.match(r"^\d{14}$", code_clean):
            return "siret"
        rna_clean = re.sub(r"[\s-]", "", code.upper())
        if re.match(r"^W\d{8}$", rna_clean):
            return "rna"
        return None

    def _call_api(self, url: str) -> Any:
        if requests is None:
            return None
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        url = f"https://recherche-entreprises.api.gouv.fr/search?q={quote(query)}"
        data = self._call_api(url)
        if data:
            return data.get("results", [])
        return []

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN, SIRET, or RNA."""
        if not code:
            return None
        code_type = self._detect_code_type(code)
        if not code_type:
            return None
        code_clean = re.sub(r"[\s-]", "", code)
        if code_type == "siren":
            url = f"https://recherche-entreprises.api.gouv.fr/search?q={code_clean}"
            data = self._call_api(url)
            if data:
                results = data.get("results", [])
                return results[0] if results else None
        elif code_type == "siret":
            url = f"https://recherche-entreprises.api.gouv.fr/search?q={code_clean}"
            data = self._call_api(url)
            if data:
                results = data.get("results", [])
                return results[0] if results else None
        else:
            rna_clean = re.sub(r"[\s-]", "", code.upper())
            url = f"https://entreprise.data.gouv.fr/api/rna/v1/id/{rna_clean}"
            data = self._call_api(url)
            if data:
                return data
        return None

