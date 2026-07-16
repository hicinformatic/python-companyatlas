from pathlib import Path
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from django_organizationatlas.models import OrganizationAtlasReferentiel
from django_organizationatlas.services.referentiel import read_csv


class ReferentielCommandTests(TestCase):
    def test_read_csv_supports_mixed_columns(self):
        with TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "referentiel.csv"
            csv_path.write_text(
                "source;description;code;country_code;category\n"
                "sample;Culture du riz;0112Z;FR;ape\n",
                encoding="utf-8",
            )

            rows = read_csv(csv_path)

        self.assertEqual(
            rows,
            [
                {
                    "category": "ape",
                    "code": "0112Z",
                    "description": "Culture du riz",
                    "country_code": "FR",
                    "source": "sample",
                }
            ],
        )

    def test_referentiel_import_imports_rows(self):
        with TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "referentiel.csv"
            csv_path.write_text(
                "category;code;description;country_code;source\n"
                "ape;0112Z;Culture du riz;FR;sample\n",
                encoding="utf-8",
            )

            call_command("referentiel", "--import", str(csv_path))

        reference = OrganizationAtlasReferentiel.objects.get()
        self.assertEqual(reference.category, "ape")
        self.assertEqual(reference.code, "0112Z")
        self.assertEqual(reference.description, "Culture du riz")
        self.assertEqual(reference.country_code, "FR")
        self.assertEqual(reference.source, "sample")

    def test_referentiel_import_updates_existing_reference(self):
        OrganizationAtlasReferentiel.objects.create(
            category="ape",
            code="0112Z",
            description="Old description",
            country_code="FR",
            source="old-source",
        )

        with TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "referentiel.csv"
            csv_path.write_text(
                "category;code;description;country_code;source\n"
                "ape;0112Z;Culture du riz;FR;new-source\n",
                encoding="utf-8",
            )

            call_command("referentiel", "--import", str(csv_path))

        self.assertEqual(OrganizationAtlasReferentiel.objects.count(), 1)
        reference = OrganizationAtlasReferentiel.objects.get()
        self.assertEqual(reference.description, "Culture du riz")
        self.assertEqual(reference.source, "new-source")

    def test_read_csv_requires_expected_columns(self):
        with TemporaryDirectory() as tmp_dir:
            csv_path = Path(tmp_dir) / "referentiel.csv"
            csv_path.write_text("code;description\n0112Z;Culture du riz\n", encoding="utf-8")

            with self.assertRaises(CommandError):
                read_csv(csv_path)

    def test_referentiel_export_exports_dump_csv(self):
        OrganizationAtlasReferentiel.objects.create(
            category="ape",
            code="0112Z",
            description="Culture du riz",
            country_code="FR",
            source="sample",
        )

        with TemporaryDirectory() as tmp_dir:
            dump_dir = Path(tmp_dir) / "referentiel" / "export"

            call_command("referentiel", "--export", str(dump_dir))

            dump_path = dump_dir / "dump.csv"

            self.assertTrue(dump_path.exists())
            self.assertEqual(
                dump_path.read_text(encoding="utf-8"),
                "category;code;description;country_code;source\n"
                "ape;0112Z;Culture du riz;FR;sample\n",
            )

    def test_admin_import_referentiel_uploads_csv(self):
        user = get_user_model().objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin",
        )
        self.client.force_login(user)

        csv_file = SimpleUploadedFile(
            "referentiel.csv",
            b"category;code;description;country_code;source\n"
            b"ape;0112Z;Culture du riz;FR;sample\n",
            content_type="text/csv",
        )
        url = reverse("admin:django_organizationatlas_organizationatlasreferentiel_import_referentiel")

        response = self.client.post(url, {"csv_file": csv_file, "_import": "Import"})

        self.assertRedirects(
            response,
            reverse("admin:django_organizationatlas_organizationatlasreferentiel_changelist"),
        )
        self.assertTrue(
            OrganizationAtlasReferentiel.objects.filter(
                category="ape",
                code="0112Z",
                description="Culture du riz",
                country_code="FR",
                source="sample",
            ).exists()
        )
