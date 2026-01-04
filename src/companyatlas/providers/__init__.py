from typing import Any

from providerkit import ProviderBase


class CompanyAtlasProvider(ProviderBase):
    config_prefix = "COMPANYATLAS"
    services = [
        "search_company",
        "search_company_by_code",
        "get_company_documents",
        "get_company_events",
    ]

    def _get_nested_value(self, data: dict[str, Any], path: str, default: Any = None) -> Any:
        if not path:
            return default
        keys = path.split(".")
        val: Any = data
        for k in keys:
            if not isinstance(val, dict):
                return default
            val = val.get(k)
            if val is None:
                return default
        return val

    def _normalize_recursive(self, data: dict[str, Any], field: str, source: str | tuple[str, ...] | None) -> Any:
        if source is None:
            return None
        if isinstance(source, tuple):
            for path in source:
                value = self._normalize_recursive(data, field, path)
                if value is not None:
                    return value
            return None
        if isinstance(source, str):
            if "." in source:
                return self._get_nested_value(data, source)
            return data.get(source)
        return source

    def normalize(self, fields: list[str], data: dict[str, Any], fields_associations: dict[str, str | tuple[str, ...] | None] | None = None) -> dict[str, Any]:
        if fields_associations is None:
            fields_associations = getattr(self, "fields_associations", {})
        normalized: dict[str, Any] = {}
        for field in fields:
            normalize_method = getattr(self, f"get_normalize_{field}", None)
            if normalize_method and callable(normalize_method):
                value = normalize_method(data)
            else:
                source = fields_associations.get(field)
                value = self._normalize_recursive(data, field, source)
            if value is not None:
                normalized[field] = value
        return normalized


__all__ = [CompanyAtlasProvider]