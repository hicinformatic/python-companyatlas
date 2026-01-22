from typing import Any, cast

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
    documentation_url = "https://docs.huwise.com"
    site_url = "https://huwise.com"
    status_url = None
    priority = 3

    fields_associations = {
        "reference": ("identifiantassociationunitelegale", "siret", "siren"),
        "denomination": ("denominationunitelegale", "denominationusuelleetablissement"),
    }

    def _call_api(self, query: str) -> dict[str, Any]:
        dataset_id = self._get_config_or_env("SIREN_DATASET_ID", default="economicref-france-sirene-v3")
        base_url = self._get_config_or_env("BASE_URL", default="https://hub.huwise.com")
        url = f"{base_url}/api/explore/v2.1/catalog/datasets/{dataset_id}/records/"
        params = {"where": f"search({query})", "limit": 20, "lang": "fr", "offset": 0, "timezone": "Europe/Paris"}
        headers: dict[str, str] = {}
        response = requests.get(url, params=params, headers=headers, timeout=10)  # type: ignore[name-defined]
        response.raise_for_status()
        return cast('dict[str, Any]', response.json())

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        query_str = f'"{query}"'
        data = self._call_api(query_str)
        results = data.get("results", [])
        return cast('list[dict[str, Any]]', results)

    def search_company_by_reference(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None

        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        query_str = f'"{siren}"'
        data = self._call_api(query_str)
        results = data.get("results", [])
        return results[0] if results else None


