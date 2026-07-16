"""Organization models."""

from .address import OrganizationAtlasAddress
from .organization import OrganizationAtlasOrganization
from .data import OrganizationAtlasData
from .delegation import OrganizationAtlasDelegation
from .document import OrganizationAtlasDocument
from .event import OrganizationAtlasEvent
from .person import OrganizationAtlasPerson
from .referentiel import OrganizationAtlasReferentiel
from .relation import OrganizationAtlasOrganizationRelation
from .stakeholder import OrganizationAtlasStakeholderRelation
from .virtuals import (
    OrganizationAtlasProviderModel,
    OrganizationAtlasVirtualOrganization,
    OrganizationAtlasVirtualDocument,
    OrganizationAtlasVirtualEvent,
)

__all__ = [
    "OrganizationAtlasOrganization",
    "OrganizationAtlasData",
    "OrganizationAtlasDelegation",
    "OrganizationAtlasDocument",
    "OrganizationAtlasEvent",
    "OrganizationAtlasAddress",
    "OrganizationAtlasPerson",
    "OrganizationAtlasReferentiel",
    "OrganizationAtlasOrganizationRelation",
    "OrganizationAtlasStakeholderRelation",
    "OrganizationAtlasProviderModel",
    "OrganizationAtlasVirtualOrganization",
    "OrganizationAtlasVirtualDocument",
    "OrganizationAtlasVirtualEvent",
]
