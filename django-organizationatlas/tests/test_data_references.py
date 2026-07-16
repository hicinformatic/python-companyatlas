from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from django_organizationatlas.models import (
    OrganizationAtlasData,
    OrganizationAtlasOrganization,
    OrganizationAtlasReferentiel,
)


class OrganizationAtlasDataReferenceTests(TestCase):
    def setUp(self):
        self.organization = OrganizationAtlasOrganization.objects.create(
            denomination="Octolo",
            code="123456789",
            country_code="FR",
            source="test",
        )

    def test_data_resolves_reference_from_data_type_and_value(self):
        OrganizationAtlasReferentiel.objects.create(
            category="ape",
            code="62.01Z",
            description="Programmation informatique",
            country_code="FR",
            source="insee",
        )
        data = OrganizationAtlasData.objects.create(
            organization=self.organization,
            data_type="ape",
            value="62.01Z",
            country_code="FR",
            source="insee",
        )

        data = OrganizationAtlasData.objects.with_resolved_referentiel().get(pk=data.pk)

        self.assertEqual(data.sql_resolved_referentiel_description, "Programmation informatique")
        self.assertEqual(data.resolved_referentiel_description, "Programmation informatique")

    def test_legacy_referentiel_description_queryset_alias_still_works(self):
        OrganizationAtlasReferentiel.objects.create(
            category="ape",
            code="62.01Z",
            description="Programmation informatique",
            country_code="FR",
            source="insee",
        )
        data = OrganizationAtlasData.objects.create(
            organization=self.organization,
            data_type="ape",
            value="62.01Z",
            country_code="FR",
            source="insee",
        )

        data = OrganizationAtlasData.objects.with_referentiel_description().get(pk=data.pk)

        self.assertEqual(data.sql_resolved_referentiel_description, "Programmation informatique")

    def test_data_reference_is_empty_when_category_does_not_exist(self):
        data = OrganizationAtlasData.objects.create(
            organization=self.organization,
            data_type="siren",
            value="123456789",
            country_code="FR",
            source="insee",
        )

        data = OrganizationAtlasData.objects.with_resolved_referentiel().get(pk=data.pk)

        self.assertIsNone(data.sql_resolved_referentiel_description)
        self.assertEqual(data.resolved_referentiel_description, "")

    def test_data_admin_displays_resolved_reference(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )
        self.client.force_login(user)
        OrganizationAtlasReferentiel.objects.create(
            category="ape",
            code="62.01Z",
            description="Programmation informatique",
            country_code="FR",
            source="insee",
        )
        OrganizationAtlasData.objects.create(
            organization=self.organization,
            data_type="ape",
            value="62.01Z",
            country_code="FR",
            source="insee",
        )

        response = self.client.get(
            reverse("admin:django_organizationatlas_organizationatlasdata_changelist")
        )

        self.assertContains(response, "Programmation informatique")
