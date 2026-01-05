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
    config_keys = ["USERNAME", "PASSWORD"]
    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    provider_can_be_used = True

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._token: str | None = None

    fields_associations = {
        "siren": ("siren", "formality.siren", "formality.content.personneMorale.identite.entreprise.siren"),
        "rna": None,
        "siret": "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.siret",
        "denomination": "formality.content.personneMorale.identite.entreprise.denomination",
        "since": ("formality.content.personneMorale.identite.entreprise.dateImmat", "formality.content.personneMorale.identite.entreprise.dateDebutActiv"),
        "legalform": ("formality.formeJuridique", "formality.content.personneMorale.identite.entreprise.formeJuridique"),
        "ape": ("formality.content.personneMorale.identite.entreprise.codeApe", "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.codeApe"),
        "category": None,
        "slice_effective": None,
        "is_headquarter": "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.indicateurEtablissementPrincipal",
        "address_line1": (
            "formality.content.personneMorale.etablissementPrincipal.adresse",
            "formality.content.personneMorale.adresseEntreprise.adresse",
        ),
        "address_line2": None,
        "address_line3": None,
        "city": ("formality.content.personneMorale.etablissementPrincipal.adresse.commune", "formality.content.personneMorale.adresseEntreprise.adresse.commune"),
        "postal_code": ("formality.content.personneMorale.etablissementPrincipal.adresse.codePostal", "formality.content.personneMorale.adresseEntreprise.adresse.codePostal"),
        "state": ("formality.content.personneMorale.etablissementPrincipal.adresse.codeInseeCommune", "formality.content.personneMorale.adresseEntreprise.adresse.codeInseeCommune"),
        "region": None,
        "county": ("formality.content.personneMorale.etablissementPrincipal.adresse.commune", "formality.content.personneMorale.adresseEntreprise.adresse.commune"),
        "country": ("formality.content.personneMorale.etablissementPrincipal.adresse.pays", "formality.content.personneMorale.adresseEntreprise.adresse.pays"),
        "country_code": ("formality.content.personneMorale.etablissementPrincipal.adresse.codePays", "formality.content.personneMorale.adresseEntreprise.adresse.codePays"),
        "municipality": ("formality.content.personneMorale.etablissementPrincipal.adresse.commune", "formality.content.personneMorale.adresseEntreprise.adresse.commune"),
        "neighbourhood": None,
        "latitude": None,
        "longitude": None,
    }

    def get_normalize_address_line1(self, data: dict[str, Any]) -> str | None:
        """Build address_line1 from multiple fields."""
        paths = [
            "formality.content.personneMorale.etablissementPrincipal.adresse",
            "formality.content.personneMorale.adresseEntreprise.adresse",
        ]
        for path in paths:
            adresse = self._get_nested_value(data, path)
            if adresse and isinstance(adresse, dict):
                num_voie = adresse.get("numVoie")
                type_voie = adresse.get("typeVoie")
                voie = adresse.get("voie")
                parts = []
                if num_voie:
                    parts.append(str(num_voie))
                if type_voie:
                    parts.append(type_voie)
                if voie:
                    parts.append(voie)
                if parts:
                    return " ".join(parts)
        return None

    def _get_token(self) -> str | None:
        """Get authentication token from INPI API."""
        if self._token:
            return self._token
        if requests is None:
            return None
        username = self._get_config_or_env("USERNAME")
        password = self._get_config_or_env("PASSWORD")
        if not username or not password:
            return None
        try:
            response = requests.post(
                "https://registre-national-entreprises.inpi.fr/api/sso/login",
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
        try:
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def search_company(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        """Search for a company by name."""
        if not query:
            return []
        result = self._call_api(
            "https://registre-national-entreprises.inpi.fr/api/companies",
            params={"companyName": query, "page": 1, "pageSize": 20},
        )
        if not result:
            return []
        if isinstance(result, dict):
            companies = result.get("companies") or result.get("data") or []
        elif isinstance(result, list):
            companies = result
        else:
            return []
        if raw:
            return companies
        normalized = []
        for company in companies:
            normalized_result = self.normalize(self.france_fields, company)
            normalized.append(normalized_result)
        return normalized

    def search_company_by_code(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        result = self._call_api(f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}")
        if not result or not isinstance(result, dict):
            return None
        if raw:
            return result
        return self.normalize(self.france_fields, result)

