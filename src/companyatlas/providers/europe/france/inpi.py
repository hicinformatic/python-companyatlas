import re
from typing import Any

try:
    import requests
except ImportError:
    requests = None

from . import CompanyAtlasFranceProvider


class InpiProvider(CompanyAtlasFranceProvider):
    name = "inpi"
    display_name = "INPI"
    description = "Institut National de la Propriété Industrielle - Registre national des entreprises"
    required_packages = ["requests"]
    config_keys = ["API_USERNAME", "API_PASSWORD", "BASE_URL", "SSO_URL"]
    config_defaults = {
        "BASE_URL": "https://registre-national-entreprises.inpi.fr",
        "SSO_URL": "https://registre-national-entreprises.inpi.fr/api/sso/login",
    }
    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    priority = 5

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._token: str | None = None

    fields_associations = {
        "reference": (
            "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.siret",
            "siren",
            "formality.siren",
            "formality.content.personneMorale.identite.entreprise.siren"
        ),
        "denomination": "formality.content.personneMorale.identite.entreprise.denomination",
    }

    def _get_token(self) -> str | None:
        """Get authentication token from INPI API."""
        if self._token:
            return self._token
        if requests is None:
            return None
        username = self._get_config_or_env("API_USERNAME")
        password = self._get_config_or_env("API_PASSWORD")
        if not username or not password:
            return None
        try:
            response = requests.post(
                self._get_config_or_env("SSO_URL"),
                json={"username": username, "password": password},
                headers={"Content-Type": "application/json"},
                timeout=10,
            )
            response.raise_for_status()
            data = response.json()
            self._token = data.get("token") or data.get("access_token")
            return self._token
        except Exception:
            return None

    def _call_api(self, url: str, params: dict[str, Any] | None = None) -> dict[str, Any] | list[dict[str, Any]] | None:
        """Make authenticated API call."""
        if requests is None:
            return None
        token = self._get_token()
        if not token:
            return None
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()


    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        result = self._call_api(
            f"{self._get_config_or_env('BASE_URL')}/api/companies",
            params={"companyName": query, "page": 1, "pageSize": 20},
        )
        if not result:
            return []
        if isinstance(result, dict):
            return result.get("companies") or result.get("data") or []
        elif isinstance(result, list):
            return result

    def search_company_by_reference(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        result = self._call_api(f"{self._get_config_or_env('BASE_URL')}/api/companies/{siren}")
        if not result or not isinstance(result, dict):
            return None
        if raw:
            return result
        return self.normalize(self.france_fields, result)

