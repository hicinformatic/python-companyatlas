from typing import Any, cast

import requests

from . import OrganizationAtlasFranceProvider


class InpiProvider(OrganizationAtlasFranceProvider):
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

    _address_prefixes = (
        "content.personneMorale.adresseEntreprise.adresse",
        "content.personneMorale.etablissementPrincipal.adresse",
        "content.personnePhysique.etablissementPrincipal.adresse",
        "content.personnePhysique.adresseEntreprise.adresse",
        # Legacy RNE wrapper (pre-2023 payloads)
        "formality.content.personneMorale.adresseEntreprise.adresse",
        "formality.content.personneMorale.etablissementPrincipal.adresse",
        "formality.content.personnePhysique.etablissementPrincipal.adresse",
        "formality.content.personnePhysique.adresseEntreprise.adresse",
    )

    fields_associations = {
        "reference": (
            "content.personneMorale.etablissementPrincipal.descriptionEtablissement.siret",
            "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.siret",
            "content.personnePhysique.etablissementPrincipal.descriptionEtablissement.siret",
            "formality.content.personnePhysique.etablissementPrincipal.descriptionEtablissement.siret",
            "siren",
            "formality.siren",
            "content.personneMorale.identite.entreprise.siren",
            "content.personnePhysique.identite.entreprise.siren",
            "formality.content.personneMorale.identite.entreprise.siren",
            "formality.content.personnePhysique.identite.entreprise.siren",
        ),
        "denomination": (
            "content.personneMorale.identite.entreprise.denomination",
            "content.personnePhysique.identite.entreprise.denomination",
            "content.personneMorale.identite.description.sigle",
            "content.personnePhysique.etablissementPrincipal.descriptionEtablissement.nomCommercial",
            "content.personneMorale.etablissementPrincipal.descriptionEtablissement.nomCommercial",
            "companyName",
            "formality.content.personneMorale.identite.entreprise.denomination",
            "formality.content.personnePhysique.identite.entreprise.denomination",
        ),
        "legalform": (
            "formeJuridique",
            "content.natureCreation.formeJuridique",
            "content.personneMorale.identite.entreprise.formeJuridique",
            "content.personnePhysique.identite.entreprise.formeJuridique",
            "formality.content.natureCreation.formeJuridique",
            "formality.content.personneMorale.identite.entreprise.formeJuridique",
            "formality.content.personnePhysique.identite.entreprise.formeJuridique",
        ),
        "ape": (
            "content.personneMorale.identite.entreprise.codeApe",
            "content.personnePhysique.identite.entreprise.codeApe",
            "content.personneMorale.etablissementPrincipal.descriptionEtablissement.codeApe",
            "content.personnePhysique.etablissementPrincipal.descriptionEtablissement.codeApe",
            "formality.content.personneMorale.identite.entreprise.codeApe",
            "formality.content.personnePhysique.identite.entreprise.codeApe",
            "formality.content.personneMorale.etablissementPrincipal.descriptionEtablissement.codeApe",
            "formality.content.personnePhysique.etablissementPrincipal.descriptionEtablissement.codeApe",
        ),
        "slice_effective": (
            "content.personneMorale.identite.entreprise.trancheEffectifs",
            "content.personnePhysique.identite.entreprise.trancheEffectifs",
            "formality.content.personneMorale.identite.entreprise.trancheEffectifs",
            "formality.content.personnePhysique.identite.entreprise.trancheEffectifs",
        ),
        "category": (
            "formeJuridique",
            "content.natureCreation.formeJuridique",
            "content.personneMorale.identite.entreprise.formeJuridique",
            "content.personnePhysique.identite.entreprise.formeJuridique",
            "formality.content.natureCreation.formeJuridique",
            "formality.content.personneMorale.identite.entreprise.formeJuridique",
            "formality.content.personnePhysique.identite.entreprise.formeJuridique",
        ),
    }

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._token: str | None = None

    def _get_token(self) -> str | None:
        if self._token:
            return self._token
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
        token = self._get_token()
        if not token:
            return None
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return cast("dict[str, Any] | list[dict[str, Any]]", response.json())

    def _content_root(self, data: dict[str, Any] | None) -> dict[str, Any] | None:
        if not isinstance(data, dict):
            return None
        content = data.get("content")
        if isinstance(content, dict):
            return content
        return self._get_nested_value(data, "formality.content")

    def _principal_establishment(self, data: dict[str, Any]) -> dict[str, Any] | None:
        content = self._content_root(data)
        if not content:
            return None
        for person_key in ("personneMorale", "personnePhysique"):
            person = content.get(person_key)
            if not isinstance(person, dict):
                continue
            principal = person.get("etablissementPrincipal")
            if isinstance(principal, dict):
                return principal
            for key in ("autresEtablissements", "etablissements"):
                establishments = person.get(key)
                if not isinstance(establishments, list):
                    continue
                for establishment in establishments:
                    if not isinstance(establishment, dict):
                        continue
                    description = establishment.get("descriptionEtablissement") or {}
                    if description.get("indicateurEtablissementPrincipal"):
                        return establishment
                if establishments and isinstance(establishments[0], dict):
                    return establishments[0]
        return None

    def _person_name_from_description(self, description: dict[str, Any] | None) -> str | None:
        if not isinstance(description, dict):
            return None
        prenoms = description.get("prenoms") or []
        if isinstance(prenoms, str):
            prenoms = [prenoms]
        first = " ".join(str(p) for p in prenoms if p)
        last = description.get("nomUsage") or description.get("nom")
        parts = [p for p in [first, last] if p]
        return " ".join(parts) if parts else None

    def _denomination_from_entrepreneur(self, data: dict[str, Any]) -> str | None:
        for prefix in (
            "content.personnePhysique.identite.entrepreneur",
            "formality.content.personnePhysique.identite.entrepreneur",
        ):
            entrepreneur = self._get_nested_value(data, prefix)
            if not isinstance(entrepreneur, dict):
                continue
            name = self._person_name_from_description(entrepreneur.get("descriptionPersonne"))
            if name:
                return name
            conjoint = entrepreneur.get("conjoint")
            if isinstance(conjoint, dict):
                name = self._person_name_from_description(conjoint.get("descriptionPersonne"))
                if name:
                    return name
        return None

    def get_normalize_denomination(self, data: dict[str, Any]) -> str | None:
        denomination = self._get_nested_value(data, self.fields_associations["denomination"])
        if denomination:
            return str(denomination)

        establishment = self._principal_establishment(data)
        if establishment:
            description = establishment.get("descriptionEtablissement") or {}
            for key in ("nomCommercial", "enseigne", "nomExploitation"):
                value = description.get(key)
                if value:
                    return str(value)

        person_name = self._denomination_from_entrepreneur(data)
        if person_name and establishment:
            description = establishment.get("descriptionEtablissement") or {}
            trade_name = description.get("nomCommercial") or description.get("enseigne")
            if trade_name and trade_name.upper() not in person_name.upper():
                return f"{person_name} ({trade_name})"
        return person_name

    def get_normalize_address(self, data: dict[str, Any]) -> str | None:
        establishment = self._principal_establishment(data)
        if establishment:
            addr = establishment.get("adresse")
            if isinstance(addr, dict):
                return self._build_address_str(
                    addr.get("numVoie"),
                    addr.get("typeVoie"),
                    addr.get("voie"),
                    addr.get("codePostal"),
                    addr.get("commune"),
                    complementLocalisation=addr.get("complementLocalisation"),
                )
        for prefix in self._address_prefixes:
            addr = self._get_nested_value(data, prefix)
            if addr:
                return self._build_address_str(
                    addr.get("numVoie"),
                    addr.get("typeVoie"),
                    addr.get("voie"),
                    addr.get("codePostal"),
                    addr.get("commune"),
                    complementLocalisation=addr.get("complementLocalisation"),
                )
        return None

    def _build_address_str(self, numero, type_voie, libelle, code_postal, commune, country=None, complementLocalisation=None):
        line1 = [p for p in [numero, type_voie, libelle] if p]
        line2_parts = [p for p in [str(code_postal) if code_postal else None, commune] if p]
        ad1 = " ".join(str(p) for p in line1) if line1 else None
        ad2 = " ".join(line2_parts) if line2_parts else None
        parts = [f for f in [ad1, complementLocalisation, ad2] if f]
        return ", ".join(parts) if parts else None

    def get_normalize_description(self, data: dict[str, Any]) -> str | None:
        activite = (
            self._get_nested_value(data, "content.personneMorale.identite.entreprise.activitePrincipale")
            or self._get_nested_value(data, "content.personnePhysique.identite.entreprise.activitePrincipale")
            or self._get_nested_value(data, "formality.content.personneMorale.identite.entreprise.activitePrincipale")
            or self._get_nested_value(data, "formality.content.personnePhysique.identite.entreprise.activitePrincipale")
        )
        nature = (
            self._get_nested_value(data, "content.personneMorale.identite.entreprise.natureJuridique")
            or self._get_nested_value(data, "content.personnePhysique.identite.entreprise.natureJuridique")
            or self._get_nested_value(data, "formality.content.personneMorale.identite.entreprise.natureJuridique")
            or self._get_nested_value(data, "formality.content.personnePhysique.identite.entreprise.natureJuridique")
        )
        parts = [p for p in [activite, nature] if p]
        return " - ".join(parts) if parts else None

    def _has_denomination(self, data: dict[str, Any]) -> bool:
        return bool(self.get_normalize_denomination(data))

    def _hydrate_company(self, item: dict[str, Any] | str) -> dict[str, Any] | None:
        if isinstance(item, str):
            return self.search_organization_by_reference(item)
        if not isinstance(item, dict):
            return None
        if self._has_denomination(item):
            return item
        siren = item.get("siren")
        if not siren:
            siren = self._get_nested_value(
                item,
                (
                    "content.personneMorale.identite.entreprise.siren",
                    "formality.content.personneMorale.identite.entreprise.siren",
                ),
            )
        if siren:
            detail = self.search_organization_by_reference(str(siren))
            if detail:
                return detail
        return item

    def _companies_api_url(self) -> str:
        return f"{self._get_config_or_env('BASE_URL')}/api/companies"

    def _extract_companies(self, result: dict[str, Any] | list[dict[str, Any]] | None) -> list[dict[str, Any]]:
        if not result:
            return []
        if isinstance(result, list):
            return result
        if isinstance(result, dict):
            for key in ("companies", "organizations", "data"):
                items = result.get(key)
                if isinstance(items, list):
                    return items
        return []

    def _matches_query(self, item: dict[str, Any], query: str) -> bool:
        if not query:
            return True
        query = query.casefold()
        candidates = [
            self.get_normalize_denomination(item),
            item.get("companyName"),
            self._get_nested_value(item, "content.personneMorale.identite.entreprise.denomination"),
            self._get_nested_value(item, "formality.content.personneMorale.identite.entreprise.denomination"),
            self._get_nested_value(item, "content.personnePhysique.etablissementPrincipal.descriptionEtablissement.nomCommercial"),
            self._get_nested_value(item, "formality.content.personnePhysique.etablissementPrincipal.descriptionEtablissement.nomCommercial"),
        ]
        return any(query in str(candidate).casefold() for candidate in candidates if candidate)

    def search_organization(self, query: str, raw: bool = False, **kwargs: Any) -> list[dict[str, Any]]:
        if not query:
            return []
        if self.is_siren(query) or self.is_siret(query):
            detail = self.search_organization_by_reference(query, raw=raw, **kwargs)
            return [detail] if detail else []
        result = self._call_api(
            self._companies_api_url(),
            params={"companyName": query, "page": 1, "pageSize": 20},
        )
        companies = self._extract_companies(result)
        hydrated: list[dict[str, Any]] = []
        for item in companies:
            company = self._hydrate_company(item)
            if company:
                hydrated.append(company)
        if hydrated:
            return hydrated

        result = self._call_api(
            self._companies_api_url(),
            params={"search": query, "page": 1, "pageSize": 20},
        )
        hydrated = []
        for item in self._extract_companies(result):
            if not self._matches_query(item, query):
                continue
            company = self._hydrate_company(item)
            if company:
                hydrated.append(company)
        return hydrated

    def search_organization_by_reference(self, code: str, raw: bool = False, **kwargs: Any) -> dict[str, Any] | None:
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        return self._call_api(f"{self._companies_api_url()}/{siren}")
