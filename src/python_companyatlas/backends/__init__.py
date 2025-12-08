"""Backend system for retrieving company/entity data by country.

Backends are organized by continent/country hierarchy:
    backends/
        base.py              # Generic base functions
        europe/
            france/
                base.py      # French-specific base functions
                insee.py     # INSEE SIRENE database
                entdatagouv.py  # data.gouv.fr entities
"""

from .base import BaseBackend

# Import country-specific backends
from .europe.france import (
    FrenchBaseBackend,
    INSEEBackend,
    EntDataGouvBackend,
    PappersBackend,
    InfogreffeBackend,
    OpendatasoftBackend,
)

__all__ = [
    "BaseBackend",
    "FrenchBaseBackend",
    "INSEEBackend",
    "EntDataGouvBackend",
    "PappersBackend",
    "InfogreffeBackend",
    "OpendatasoftBackend",
]

