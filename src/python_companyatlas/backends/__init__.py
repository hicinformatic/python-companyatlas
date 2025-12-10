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

from .base import BaseBackend, get_country_flag_emoji, get_country_flag_image_base64

# Import country-specific backends
from .europe.france import (
    CCIBackend,
    EntDataGouvBackend,
    EspaceDocsBackend,
    FrenchBaseBackend,
    InfogreffeBackend,
    INPIBackend,
    INSEEBackend,
    OpendatasoftBackend,
    PappersBackend,
    PharowBackend,
    SocieteComBackend,
    SocieteDataBackend,
    SocieteInfoBackend,
    VerifBackend,
)

# Import helpers
from .helpers import (
    get_all_backend_classes,
    get_all_backends,
    get_backends,
    get_backends_by_continent,
    get_backends_by_country,
    get_backends_sorted,
)

__all__ = [
    "BaseBackend",
    "get_country_flag_emoji",
    "get_country_flag_image_base64",
    "FrenchBaseBackend",
    "INSEEBackend",
    "EntDataGouvBackend",
    "PappersBackend",
    "InfogreffeBackend",
    "OpendatasoftBackend",
    "INPIBackend",
    "SocieteComBackend",
    "VerifBackend",
    "SocieteInfoBackend",
    "CCIBackend",
    "SocieteDataBackend",
    "PharowBackend",
    "EspaceDocsBackend",
    "get_all_backend_classes",
    "get_all_backends",
    "get_backends",
    "get_backends_sorted",
    "get_backends_by_continent",
    "get_backends_by_country",
]
