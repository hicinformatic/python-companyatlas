import re
from typing import Any

from ....fields.france import (
    FRANCE_FIELDS_DESCRIPTIONS,
    FR_SEARCH_COMPANY_FIELDS as FR_SEARCH_COMPANY_FIELDS,
)
from .. import OrganizationAtlasEuropeProvider

# (pattern, max_length, uppercase)
_CODE_PATTERNS: dict[str, tuple[str, int, bool]] = {
    "siret": (r"^\d{14}$", 14, False),
    "siren": (r"^\d{9}$", 9, False),
    "rna":   (r"^W\d{8}$", 9, True),
}


class OrganizationAtlasFranceProvider(OrganizationAtlasEuropeProvider):
    geo_code = "FR"
    geo_country = "france"
    abstract = True
    france_fields = list(FRANCE_FIELDS_DESCRIPTIONS.keys())

    # ------------------------------------------------------------------ #
    # Code validation & formatting                                         #
    # ------------------------------------------------------------------ #

    def _clean_code(self, code: str, upper: bool = False) -> str:
        if not code:
            return ""
        if upper:
            code = code.upper()
        return re.sub(r"[\s-]", "", code)

    def _matches_pattern(self, code: str, kind: str) -> bool:
        pattern, _, upper = _CODE_PATTERNS[kind]
        return bool(re.match(pattern, self._clean_code(code, upper)))

    def _format_code(self, code: str, kind: str) -> str:
        _, length, upper = _CODE_PATTERNS[kind]
        cleaned = self._clean_code(code, upper)
        return cleaned[:length] if len(cleaned) >= length else cleaned

    def is_siret(self, query: str) -> bool:
        return bool(query) and self._matches_pattern(query, "siret")

    def is_siren(self, query: str) -> bool:
        return bool(query) and self._matches_pattern(query, "siren")

    def is_rna(self, query: str) -> bool:
        return bool(query) and self._matches_pattern(query, "rna")

    def _validate_siret(self, siret: str) -> bool:
        return self._matches_pattern(siret, "siret")

    def _validate_siren(self, siren: str) -> bool:
        return self._matches_pattern(siren, "siren")

    def _validate_rna(self, rna: str) -> bool:
        return self._matches_pattern(rna, "rna")

    def _format_siret(self, siret: str) -> str:
        return self._format_code(siret, "siret")

    def _format_siren(self, siren: str) -> str:
        return self._format_code(siren, "siren")

    def _format_rna(self, rna: str) -> str:
        return self._format_code(rna, "rna")

    def _format_ape(self, ape: Any) -> str | None:
        if not ape:
            return None
        code = re.sub(r"[\s.]", "", str(ape)).upper()
        if len(code) == 5 and code[:4].isdigit() and code[4].isalpha():
            return f"{code[:2]}.{code[2:]}"
        return str(ape)

    def _detect_code_type(self, code: str) -> str | None:
        for kind in ("siret", "siren", "rna"):
            if self._matches_pattern(code, kind):
                return kind
        return None

    # ------------------------------------------------------------------ #
    # Address helpers                                                      #
    # ------------------------------------------------------------------ #

    def _build_address_str(
        self,
        numero: Any,
        type_voie: Any,
        libelle: Any,
        code_postal: Any,
        commune: Any,
        country: str | None = None,
    ) -> str | None:
        line1 = [p for p in [numero, type_voie, libelle] if p]
        parts: list[str] = []
        if line1:
            parts.append(" ".join(str(p) for p in line1))
        if code_postal:
            parts.append(str(code_postal))
        if commune:
            parts.append(str(commune))
        if country:
            parts.append(country)
        return ", ".join(parts) if parts else None

    def _build_address_json(
        self,
        numero: Any,
        type_voie: Any,
        libelle: Any,
        code_postal: Any,
        commune: Any,
    ) -> dict[str, Any] | None:
        line1 = [p for p in [numero, type_voie, libelle] if p]
        address_line1 = " ".join(str(p) for p in line1) if line1 else None
        if not address_line1 and not code_postal and not commune:
            return None
        return {
            "address_line1": address_line1,
            "postal_code": code_postal,
            "city": commune,
            "country": self.geo_country,
            "country_code": self.geo_code,
        }

    # ------------------------------------------------------------------ #
    # ProviderKit hook                                                     #
    # ------------------------------------------------------------------ #

    def get_normalize_reference(self, data: dict[str, Any]) -> str | None:
        reference = self._get_nested_value(data, self.fields_associations.get("reference", "reference"))
        return str(reference) if reference else None

    def get_normalize_ape(self, data: dict[str, Any]) -> str | None:
        ape = self._get_nested_value(data, self.fields_associations.get("ape", "ape"))
        return self._format_ape(ape)

    def get_normalize_source_field(self, data: dict[str, Any]) -> str | None:
        reference = self.get_normalize_reference(data)
        if reference:
            return self._detect_code_type(reference)

        cache = self._service_results_cache.get("search_organization_by_reference", {})
        kwargs = cache.get("kwargs", {})
        code = kwargs.get("code", "")
        return self._detect_code_type(code)
