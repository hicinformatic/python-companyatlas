"""French company data backends.

This module contains backends for retrieving French company data from various sources:
- INSEE SIRENE database
- data.gouv.fr entities
- Pappers (company data aggregator)
- Infogreffe (commercial court registry)
- Opendatasoft (open data platform)
- INPI (Institut National de la Propriété Industrielle)
- Societe.com (company data aggregator)
- Pharow (B2B data aggregation)
"""

from .base import FrenchBaseBackend
from .bodacc import BODACCBackend
from .entdatagouv import EntDataGouvBackend
from .infogreffe import InfogreffeBackend
from .inpi import INPIBackend
from .insee import INSEEBackend
from .opendatasoft import OpendatasoftBackend
from .pappers import PappersBackend
from .pharow import PharowBackend
from .societecom import SocieteComBackend

__all__ = [
    "FrenchBaseBackend",
    "BODACCBackend",
    "INSEEBackend",
    "EntDataGouvBackend",
    "PappersBackend",
    "InfogreffeBackend",
    "OpendatasoftBackend",
    "INPIBackend",
    "SocieteComBackend",
    "PharowBackend",
]
