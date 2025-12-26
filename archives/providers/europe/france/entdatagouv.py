"""data.gouv.fr entities backend.

This backend provides access to French entity data from data.gouv.fr,
including associations (RNA), companies, and official publications.
"""

from typing import Any
from urllib.parse import quote, urlencode

try:
    import requests
except ImportError:
    requests = None

from .base import FrenchBaseBackend


class EntDataGouvBackend(FrenchBaseBackend):
    """Backend for data.gouv.fr entities.

    Provides access to French entity data from the official data.gouv.fr platform,
    including associations (RNA) and company data.
    """

    name = "entdatagouv"
    display_name = "data.gouv.fr"
    description_text = "French open data platform for public entities and datasets"

    config_keys = []
    required_packages = ["requests"]

    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    request_cost = {
        "data": "free",
        "documents": "free",
        "events": "free",
    }

    documentation_url = "https://www.data.gouv.fr/api"
    site_url = "https://www.data.gouv.fr"
    status_url = None
    api_url = "https://www.data.gouv.fr/api/1"

    urls = {
        "siren": "https://recherche-entreprises.api.gouv.fr/search?q=%s",
        "siret": "https://recherche-entreprises.api.gouv.fr/search?q=%s",
        "rna": "https://entreprise.data.gouv.fr/api/rna/v1/id/%s",
        "text": "https://recherche-entreprises.api.gouv.fr/search?q=%s",
    }

    fields_association = {
        "siren": "siren",
        "rna": "id_association",
        "siret": "siege.siret",
        "denomination": ("nom_complet", "nom_raison_sociale"),
        "since": ("date_creation", "date_creation_entreprise"),
        "legalform": "nature_juridique",
        "ape": "siege.activite_principale",
        "category": "categorie_entreprise",
        "slice_effective": "siege.tranche_effectif_salarie",
        "siege": "siege.est_siege",
    }

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize data.gouv.fr backend."""
        super().__init__(config)
        self.base_url = self._get_config_or_env("base_url", default=self.api_url)

    def _build_query_params(self, **kwargs) -> dict[str, Any]:
        """Filter out None values from kwargs."""
        params = {}
        for key, value in kwargs.items():
            if value is not None:
                params[key] = value
        return params

    def _build_url_with_params(self, base_url: str, **kwargs) -> str:
        """Build URL with query parameters from kwargs."""
        params = self._build_query_params(**kwargs)
        if params:
            query_string = urlencode(params)
            separator = "&" if "?" in base_url else "?"
            return f"{base_url}{separator}{query_string}"
        return base_url

    def _get_search_type(self, query: str) -> str:
        """Detect search type from query."""
        if self.validate_siren(query):
            return "siren"
        if len(query) == 14 and query.isdigit():
            return "siret"
        if self.validate_rna(query):
            return "rna"
        return "text"

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for entities by name on data.gouv.fr.

        Args:
            name: Company name to search for
            **kwargs: Additional query parameters (e.g., is_siege='yes', per_page=20, raw=True)
                - raw: If True, return raw API response without normalization
        """
        if not name or not isinstance(name, str):
            return []

        if requests is None:
            return []

        raw = kwargs.pop("raw", False)
        search_type = self._get_search_type(name)
        base_url_template = self.urls.get(search_type, self.urls["text"])
        base_url = base_url_template % quote(name)
        url = self._build_url_with_params(base_url, **kwargs)

        try:
            response = requests.get(url, timeout=10, verify=True)
            response.raise_for_status()
            data = response.json()
            results = data.get("results", [])
            limit = kwargs.get("limit", 20)
            raw_results = results[:limit] if limit else results
            if raw:
                return raw_results
            return self.normalize_results(raw_results)
        except requests.exceptions.RequestException:
            return []
        except (ValueError, KeyError):
            return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for an entity by SIREN or RNA on data.gouv.fr.

        Args:
            code: SIREN or RNA identifier
            code_type: Type of identifier ('siren' or 'rna')
            **kwargs: Additional query parameters (e.g., is_siege='yes', raw=True)
                - raw: If True, return raw API response without normalization
        """
        if not code:
            return None

        if requests is None:
            return None

        raw = kwargs.pop("raw", False)
        if not code_type:
            code_type = self.detect_identifier_type(code)

        if code_type == "siren":
            siren = self.format_siren(code)
            if not self.validate_siren(siren):
                return None
            base_url = self.urls["siren"] % quote(siren)
            url = self._build_url_with_params(base_url, **kwargs)
            try:
                response = requests.get(url, timeout=10, verify=True)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])
                if results:
                    if raw:
                        return results[0]
                    return self._normalize_result(results[0])
                return None
            except requests.exceptions.RequestException:
                return None
            except (ValueError, KeyError):
                return None

        elif code_type == "rna":
            rna = self.format_rna(code)
            if not self.validate_rna(rna):
                return None
            base_url = self.urls["rna"] % quote(rna)
            url = self._build_url_with_params(base_url, **kwargs)
            try:
                response = requests.get(url, timeout=10, verify=True)
                response.raise_for_status()
                data = response.json()
                if raw:
                    return data
                return self._normalize_result(data)
            except requests.exceptions.RequestException:
                return None
            except (ValueError, KeyError):
                return None

        return None

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to data.gouv.fr."""
        if requests is None:
            return None
        try:
            response = requests.get(endpoint, params=params, timeout=10, verify=True)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None
        except (ValueError, KeyError):
            return None
