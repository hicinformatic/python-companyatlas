from .address import OrganizationAtlasAddressAdmin
from .organization import OrganizationAtlasOrganizationAdmin
from .data import OrganizationAtlasDataAdmin
from .delegation import OrganizationAtlasDelegationAdmin
from .document import OrganizationDocumentAdmin
from .event import OrganizationEventAdmin
from .person import OrganizationAtlasPersonAdmin
from .referentiel import OrganizationAtlasReferentielAdmin
from .virtuals.organization import OrganizationAtlasVirtualOrganizationAdmin
from .virtuals.document import OrganizationAtlasVirtualDocumentAdmin
from .virtuals.event import OrganizationAtlasVirtualEventAdmin
from .virtuals.provider import OrganizationAtlasProviderModel

__all__ = [
    "OrganizationAtlasOrganizationAdmin",
    "OrganizationAtlasDataAdmin",
    "OrganizationAtlasDelegationAdmin",
    "OrganizationAtlasAddressAdmin",
    "OrganizationDocumentAdmin",
    "OrganizationEventAdmin",
    "OrganizationAtlasPersonAdmin",
    "OrganizationAtlasReferentielAdmin",
    "OrganizationAtlasProviderModel",
    "OrganizationAtlasVirtualOrganizationAdmin",
    "OrganizationAtlasVirtualDocumentAdmin",
    "OrganizationAtlasVirtualEventAdmin",
]
