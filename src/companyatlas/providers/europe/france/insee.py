import re
from typing import Any
from urllib.parse import urlencode

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class InseeProvider(CompanyAtlasFranceProvider):
    name = "insee"
    display_name = "INSEE SIRENE"
    description = "Official French company registry (SIRENE database)"
    required_packages = ["requests"]
    config_keys = ["INSEE_API_KEY"]
    documentation_url = "https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/list-apis.jag"
    site_url = "https://www.insee.fr"
    status_url = "https://api.insee.fr/status"
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

    def _call_api(self, query: str) -> list[dict[str, Any]]:
        if requests is None:
            return []
        api_key = self._get_config_or_env("INSEE_API_KEY")
        if not api_key:
            return []
        url = f"https://api.insee.fr/entreprises/sirene/V3/api-sirene/3.11/siret?{urlencode({'q': query, 'nombre': 20})}"
        headers = {"Accept": "application/json", "X-INSEE-Api-Key-Integration": api_key}
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            return data.get("etablissements", [])
        except Exception:
            return []

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        query_str = f'denominationUniteLegale:"{query}"+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true'
        return self._call_api(query_str)

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN, SIRET, or RNA."""
        if not code:
            return None
        code_type = self._detect_code_type(code)
        if not code_type:
            return None
        code_clean = re.sub(r"[\s-]", "", code)
        if code_type == "siren":
            query_str = f"siren:{code_clean}+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true"
        elif code_type == "siret":
            query_str = f"siret:{code_clean}+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true"
        else:
            rna_clean = re.sub(r"[\s-]", "", code.upper())
            query_str = f"identifiantAssociationUniteLegale:{rna_clean}+AND+etablissementSiege:true+AND+etatAdministratifUniteLegale:A"
        results = self._call_api(query_str)
        return results[0] if results else None
