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

    fields_associations = {
        "siren": "siren",
        "rna": "complements.identifiant_association",
        "siret": "siege.siret",
        "is_association": "complements.est_association",
        "denomination": ("nom_complet", "nom_raison_sociale"),
        "since": "date_creation",
        "legalform": "nature_juridique",
        "ape": ("activite_principale", "siege.activite_principale"),
        "category": "categorie_entreprise",
        "slice_effective": "tranche_effectif_salarie",
        "is_headquarter": "est_siege",
        "address_line2": "siege.complement_adresse",
        "address_line3": "siege.complement_adresse2",
        "city": "siege.libelle_commune",
        "postal_code": "siege.code_postal",
        "state": "siege.departement",
        "region": "siege.region",
        "county": "siege.commune",
        "country": "siege.pays",
        "country_code": "siege.code_pays",
        "municipality": "siege.commune",
        "neighbourhood": "siege.commune",
        "latitude": "siege.latitude",
        "longitude": "siege.longitude",
    }

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

    def get_normalize_address_line1(self, data: dict[str, Any]) -> str | None:
        nv = self._get_nested_value(data, "siege.numero_voie")
        tv = self._get_nested_value(data, "siege.type_voie")
        lv = self._get_nested_value(data, "siege.libelle_voie")
        return f"{nv} {tv} {lv}"

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        url = f"https://recherche-entreprises.api.gouv.fr/search?q={quote(query)}"
        data = self._call_api(url)
        if data:
            results = data.get("results", [])
            if raw:
                return results
            normalized = []
            for result in results:
                normalized_result = self.normalize(self.france_fields, result)
                normalized.append(normalized_result)
            return normalized
        return []

    def search_company_by_code(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN, SIRET, or RNA."""
        if not code:
            return None
        code_type = self._detect_code_type(code)
        if not code_type:
            return None
        code_clean = re.sub(r"[\s-]", "", code)
        result = None
        if code_type == "siren":
            url = f"https://recherche-entreprises.api.gouv.fr/search?q={code_clean}"
            data = self._call_api(url)
            if data:
                results = data.get("results", [])
                result = results[0] if results else None
        elif code_type == "siret":
            url = f"https://recherche-entreprises.api.gouv.fr/search?q={code_clean}"
            data = self._call_api(url)
            if data:
                results = data.get("results", [])
                result = results[0] if results else None
        else:
            rna_clean = re.sub(r"[\s-]", "", code.upper())
            url = f"https://entreprise.data.gouv.fr/api/rna/v1/id/{rna_clean}"
            result = self._call_api(url)
        if result is None:
            return None
        if raw:
            return result
        return self.normalize(self.france_fields, result)

