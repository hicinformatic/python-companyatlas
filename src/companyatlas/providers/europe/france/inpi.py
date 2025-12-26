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
    config_keys = ["INPI_API_KEY", "INPI_USERNAME", "INPI_PASSWORD"]
    documentation_url = "https://www.inpi.fr/fr/services-et-outils/api"
    site_url = "https://www.inpi.fr"
    status_url = None
    provider_can_be_used = True

    def _validate_siren(self, siren: str) -> bool:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return bool(re.match(r"^\d{9}$", siren_clean))

    def _format_siren(self, siren: str) -> str:
        siren_clean = re.sub(r"[\s-]", "", siren)
        return siren_clean[:9] if len(siren_clean) >= 9 else siren_clean

    def search_company(self, query: str) -> list[dict[str, Any]]:
        """Search for a company by name."""
        return []

    def search_company_by_code(self, code: str) -> dict[str, Any] | None:
        """Search for a company by SIREN."""
        if not code:
            return None
        siren = self._format_siren(code)
        if not self._validate_siren(siren):
            return None
        return None

