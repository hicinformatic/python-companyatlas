from pathlib import Path

from django.core.management.base import BaseCommand, CommandError

from django_organizationatlas.services.referentiel import (
    export_referentiel_to_path,
    import_referentiel_from_path,
)


class Command(BaseCommand):
    help = "Import or export referentiel CSV files"

    def add_arguments(self, parser):
        parser.add_argument(
            "--export",
            nargs="?",
            const="",
            default=None,
            help="Export referentiel data to a CSV file. Defaults to referentiel/export/dump.csv",
        )
        parser.add_argument(
            "--import",
            nargs="?",
            const="",
            default=None,
            dest="import_path",
            help="CSV file or directory to import. Defaults to referentiel/import/*.csv",
        )

    def handle(self, **options):
        export = options.get("export")
        import_path = options.get("import_path")

        if export is not None and import_path is not None:
            raise CommandError("Use either --export or --import, not both")

        if export is None and import_path is None:
            raise CommandError("Use --export or --import")

        if export is not None:
            path = export or Path.cwd() / "referentiel" / "export"
            dump_path, exported_count = export_referentiel_to_path(path)
            self.stdout.write(
                self.style.SUCCESS(f"Exported {exported_count} referentiel row(s) to {dump_path}")
            )
        else:
            path = import_path or Path.cwd() / "referentiel" / "import"
            created_count, updated_count, file_count = import_referentiel_from_path(path)
            self.stdout.write(
                self.style.SUCCESS(
                    f"Imported {file_count} file(s): {created_count} created, {updated_count} updated"
                )
            )
