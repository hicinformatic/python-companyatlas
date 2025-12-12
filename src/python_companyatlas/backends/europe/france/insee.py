"""INSEE SIRENE database backend.

This backend provides access to the French INSEE SIRENE database which contains
official company registration data including SIREN numbers, company names, addresses,
and legal status.
"""

from typing import Any
from urllib.parse import quote, urlencode

try:
    import requests
except ImportError:
    requests = None

from .base import FrenchBaseBackend


class INSEEBackend(FrenchBaseBackend):
    """Backend for INSEE SIRENE database.

    Provides access to French company data from the official INSEE SIRENE registry.
    """

    name = "insee"
    display_name = "INSEE SIRENE"
    description_text = "Official French company registry (SIRENE database)"

    config_keys = ["api_key"]
    required_packages = ["requests"]

    can_fetch_documents = False
    can_fetch_events = False
    can_fetch_company_data = True

    request_cost = {
        "data": "free",
        "documents": "free",
        "events": "free",
    }

    documentation_url = (
        "https://api.insee.fr/catalogue/site/themes/wso2/subthemes/insee/pages/list-apis.jag"
    )
    site_url = "https://www.insee.fr"
    status_url = "https://api.insee.fr/status"
    api_url = "https://api.insee.fr/entreprises/sirene/V3"

    urls = {
        "siren": {
            "url": "api-sirene/3.11/siret",
            "query": 'siren:%s+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true',
        },
        "siret": {
            "url": "api-sirene/3.11/siret",
            "query": 'siret:%s+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true',
        },
        "rna": {
            "url": "api-sirene/3.11/siret",
            "query": 'identifiantAssociationUniteLegale:%s+AND+etablissementSiege:true+AND+etatAdministratifUniteLegale:A',
        },
        "text": {
            "url": "api-sirene/3.11/siret",
            "query": 'denominationUniteLegale:"%s"+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true',
        },
    }

    fields_association = {
        "siren": "siren",
        "rna": "uniteLegale.identifiantAssociationUniteLegale",
        "siret": "siret",
        "denomination": (
            "uniteLegale.denominationUniteLegale",
            "uniteLegale.nomUniteLegale",
        ),
        "ape": "uniteLegale.activitePrincipaleUniteLegale",
        "legalform": "uniteLegale.categorieJuridiqueUniteLegale",
        "since": "uniteLegale.dateCreationUniteLegale",
        "category": "uniteLegale.categorieEntreprise",
        "slice_effective": "uniteLegale.trancheEffectifsUniteLegale",
        "siege": "etablissementSiege",
    }

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize INSEE backend."""
        super().__init__(config)
        self.api_key = self._get_config_or_env("api_key")
        self.base_url = self._get_config_or_env("base_url", default="https://api.insee.fr/")

    def _get_search_type(self, query: str) -> str:
        """Detect search type from query string."""
        if self.validate_siren(query):
            return "siren"
        if self.validate_rna(query):
            return "rna"
        siret_clean = query.replace(" ", "").replace("-", "")
        if len(siret_clean) == 14 and siret_clean.isdigit():
            return "siret"
        return "text"

    def _build_query_string(self, base_query: str, query_params: dict[str, Any] | None = None) -> str:
        """Build INSEE query string with AND conditions.
        
        Args:
            base_query: Base query string (e.g., 'siren:123456789')
            query_params: Additional filters (e.g., {'etatAdministratifUniteLegale': 'A'})
        
        Returns:
            Query string in format: 'siren:123+AND+etatAdministratifUniteLegale:A+AND+etablissementSiege:true'
        """
        query_params = query_params or {}
        if not query_params:
            return base_query

        existing_conditions = base_query.split("+AND+")
        conditions_dict = {}

        for condition in existing_conditions:
            if ":" in condition:
                key, value = condition.split(":", 1)
                conditions_dict[key] = value

        for key, value in query_params.items():
            if value is not None:
                if isinstance(value, bool):
                    value_str = str(value).lower()
                else:
                    value_str = str(value)
                conditions_dict[key] = value_str

        conditions = [f"{key}:{value}" for key, value in conditions_dict.items()]
        return "+AND+".join(conditions)

    def search_by_name(self, name: str, **kwargs) -> list[dict[str, Any]]:
        """Search for companies by name in INSEE SIRENE database.
        
        Args:
            name: Company name to search for
            **kwargs: Additional query filters (e.g., etatAdministratifUniteLegale='A',
                     etablissementSiege=True, raw=True, limit=20)
                - raw: If True, return raw API response without normalization
        """
        if not name or not isinstance(name, str):
            return []

        if requests is None:
            return []

        if not self.api_key:
            return []

        raw = kwargs.pop("raw", False)
        limit = kwargs.pop("limit", 20)
        query_params = kwargs

        search_type = self._get_search_type(name)
        search_conf = self.urls.get(search_type, self.urls["text"])

        base_query = search_conf["query"] % name
        final_query = self._build_query_string(base_query, query_params)

        query_params_url = {
            "q": final_query,
            "nombre": limit,
            "debut": 0,
            "masquerValeursNulles": "true",
        }
        query_string = urlencode(query_params_url, quote_via=lambda s, safe="", encoding=None, errors=None: quote(s, safe="+", encoding=encoding, errors=errors))
        url = f"{self.base_url}{search_conf['url']}?{query_string}"

        headers = {
            "Accept": "application/json",
            "X-INSEE-Api-Key-Integration": self.api_key,
        }

        try:
            response = requests.get(url, headers=headers, timeout=10, verify=True)
            response.raise_for_status()
            data = response.json()
            results = data.get("etablissements", [])
            
            if raw:
                return results
            return self.normalize_results(results)
        except requests.exceptions.RequestException:
            return []
        except (ValueError, KeyError):
            return []

    def search_by_code(
        self, code: str, code_type: str | None = None, **kwargs
    ) -> dict[str, Any] | None:
        """Search for a company by SIREN in INSEE SIRENE database.
        
        Args:
            code: SIREN identifier
            code_type: Type of identifier (should be 'siren')
            **kwargs: Additional query filters (e.g., etatAdministratifUniteLegale='A',
                     etablissementSiege=True)
        """
        if code_type and code_type != "siren":
            raise ValueError(f"INSEE backend only supports SIREN codes, not {code_type}")

        siren = self.format_siren(code)
        if not self.validate_siren(siren):
            return None

        return None

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to INSEE SIRENE service."""
        return None

    def _parse_siret_response(self, response: dict[str, Any]) -> dict[str, Any]:
        """Parse INSEE SIRET API response into standardized format."""
        return {}
