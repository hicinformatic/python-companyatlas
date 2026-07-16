from django.core.exceptions import ValidationError
from django.test import TestCase

from django_organizationatlas.models import (
    OrganizationAtlasDelegation,
    OrganizationAtlasOrganization,
)


class OrganizationAtlasDelegationTests(TestCase):
    def setUp(self):
        self.grantor = OrganizationAtlasOrganization.objects.create(
            denomination="Grantor",
            code="111111111",
        )
        self.receiver = OrganizationAtlasOrganization.objects.create(
            denomination="Receiver",
            code="222222222",
        )

    def test_delegation_tracks_who_grants_authority_to_whom(self):
        delegation = OrganizationAtlasDelegation.objects.create(
            organization=self.grantor,
            delegation=self.receiver,
            source="test",
            country_code="FR",
        )

        self.assertEqual(self.grantor.delegations_given.get(), delegation)
        self.assertEqual(self.receiver.delegations_received.get(), delegation)

    def test_organization_cannot_delegate_to_itself(self):
        delegation = OrganizationAtlasDelegation(
            organization=self.grantor,
            delegation=self.grantor,
        )

        with self.assertRaises(ValidationError):
            delegation.full_clean()
