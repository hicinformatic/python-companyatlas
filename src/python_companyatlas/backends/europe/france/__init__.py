"""French company data backends.

This module contains backends for retrieving French company data from various sources:
- INSEE SIRENE database
- data.gouv.fr entities
- Pappers (company data aggregator)
- Infogreffe (commercial court registry)
- Opendatasoft (open data platform)
- BODACC (Bulletin Officiel des Annonces Civiles et Commerciales)
- BALO (Bulletin des Annonces Légales Obligatoires)
"""

from .base import FrenchBaseBackend
from .insee import INSEEBackend
from .entdatagouv import EntDataGouvBackend
from .pappers import PappersBackend
from .infogreffe import InfogreffeBackend
from .opendatasoft import OpendatasoftBackend

__all__ = [
    "FrenchBaseBackend",
    "INSEEBackend",
    "EntDataGouvBackend",
    "PappersBackend",
    "InfogreffeBackend",
    "OpendatasoftBackend",
]

