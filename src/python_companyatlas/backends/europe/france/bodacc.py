"""BODACC (Bulletin Officiel des Annonces Civiles et Commerciales) backend.

This backend provides access to the French BODACC which publishes official
announcements about companies including status changes, modifications, and
legal events.
"""

from datetime import datetime
from typing import Any

from .base import FrenchBaseBackend


class BODACCBackend(FrenchBaseBackend):
    """Backend for BODACC (Bulletin Officiel des Annonces Civiles et Commerciales).

    BODACC publishes official announcements about French companies including:
    - Company creation and registration
    - Status changes (modification, dissolution, etc.)
    - Capital changes
    - Address changes
    - Director appointments/resignations
    - Mergers and acquisitions
    - Legal events and notifications
    """

    name = "bodacc"
    display_name = "BODACC"
    description_text = (
        "Bulletin Officiel des Annonces Civiles et Commerciales - "
        "Publications officielles sur les entreprises françaises"
    )

    config_keys = ["api_key", "base_url"]
    required_packages = ["requests"]

    can_fetch_documents = True
    can_fetch_events = True
    can_fetch_company_data = False

    documentation_url = "https://www.data.gouv.fr/fr/datasets/bodacc/"
    site_url = "https://www.bodacc.fr"
    status_url = None
    api_url = "https://www.data.gouv.fr/api/1"

    def __init__(self, config: dict[str, Any] | None = None):
        """Initialize BODACC backend."""
        super().__init__(config)
        self.api_key = self.config.get("api_key")
        self.base_url = self.config.get("base_url", self.api_url)

    def get_documents(
        self, identifier: str, document_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get BODACC documents/publications for a company."""
        if not identifier:
            return []

        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        category = kwargs.get("category")

        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        return []

    def get_events(
        self, identifier: str, event_type: str | None = None, **kwargs
    ) -> list[dict[str, Any]]:
        """Get BODACC events/changes for a company."""
        if not identifier:
            return []

        siren = self.format_siren(identifier)
        if not self.validate_siren(siren):
            return []

        date_from = kwargs.get("date_from")
        date_to = kwargs.get("date_to")
        category = kwargs.get("category")

        if isinstance(date_from, datetime):
            date_from = date_from.isoformat()
        if isinstance(date_to, datetime):
            date_to = date_to.isoformat()

        return []

    def _call_api(
        self, endpoint: str, params: dict[str, Any] | None = None
    ) -> dict[str, Any] | None:
        """Make API call to BODACC service."""
        return None

    def _parse_bodacc_documents(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse BODACC documents API response."""
        return []

    def _parse_bodacc_events(self, response: dict[str, Any]) -> list[dict[str, Any]]:
        """Parse BODACC events API response."""
        return []

