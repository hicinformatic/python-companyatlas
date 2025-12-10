"""Main CompanyAtlas client."""

import re
from typing import Any


class CompanyAtlas:
    """Client for company information lookup and enrichment."""

    def __init__(self, api_key: str | None = None, config: dict[str, Any] | None = None):
        """Initialize CompanyAtlas client.

        Args:
            api_key: Optional API key for authentication
            config: Optional configuration dictionary
        """
        self.api_key = api_key
        self.config = config or {}

    def _validate_domain(self, domain: str) -> None:
        """Validate domain name format.

        Args:
            domain: Domain name to validate

        Raises:
            ValueError: If domain is invalid
        """
        if not domain or not isinstance(domain, str):
            raise ValueError("Domain must be a non-empty string")

        domain = domain.strip().lower()

        # Basic domain validation regex
        # Allows: alphanumeric, hyphens, dots
        # Must have at least one dot
        # TLD must be at least 2 characters
        domain_pattern = r"^([a-z0-9]([a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,}$"
        if not re.match(domain_pattern, domain):
            raise ValueError(
                f"Invalid domain format: {domain}. "
                "Domain must be a valid hostname (e.g., 'example.com')"
            )

        # Additional security: prevent overly long domains
        if len(domain) > 253:  # RFC 1035 max domain length
            raise ValueError("Domain name too long (max 253 characters)")

        # Prevent common injection patterns
        if any(char in domain for char in ["/", "\\", ":", "?", "#", "[", "]", "@", "!"]):
            raise ValueError("Domain contains invalid characters")

    def lookup(self, domain: str) -> dict[str, Any]:
        """Look up company information by domain.

        Args:
            domain: Company domain name (e.g., 'example.com')

        Returns:
            Dictionary containing company information

        Raises:
            ValueError: If domain is invalid
        """
        self._validate_domain(domain)

        # TODO: Implement actual lookup logic
        return {
            "domain": domain,
            "name": f"Company for {domain}",
            "status": "pending",
        }

    def enrich(self, company_data: dict[str, Any]) -> dict[str, Any]:
        """Enrich company data with additional information.

        Args:
            company_data: Base company information

        Returns:
            Enriched company information
        """
        # TODO: Implement enrichment logic
        enriched = company_data.copy()
        enriched["enriched"] = True
        return enriched
