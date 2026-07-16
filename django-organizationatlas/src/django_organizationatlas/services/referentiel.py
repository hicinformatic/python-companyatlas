import csv
from pathlib import Path

from django.core.management.base import CommandError

from django_organizationatlas.models import OrganizationAtlasReferentiel as Referentiel

REFERENTIEL_COLUMNS = ("category", "code", "description", "country_code", "source")
REQUIRED_COLUMNS = set(REFERENTIEL_COLUMNS)
DEFAULT_DUMP_FILENAME = "dump.csv"


def get_csv_paths(path):
    if path is None:
        raise CommandError("A path is required")

    csv_path = Path(path)

    if any(char in str(csv_path) for char in "*?["):
        return sorted(csv_path.parent.glob(csv_path.name))

    if csv_path.is_dir():
        return sorted(csv_path.glob("*.csv"))

    if not csv_path.exists():
        return []

    return [csv_path]


def get_dump_path(path):
    dump_path = Path(path)

    if dump_path.suffix.lower() == ".csv":
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        return dump_path

    dump_path.mkdir(parents=True, exist_ok=True)
    return dump_path / DEFAULT_DUMP_FILENAME


def read_csv(path):
    csv_path = Path(path)

    if not csv_path.exists():
        raise CommandError(f"CSV file not found: {csv_path}")

    with csv_path.open(encoding="utf-8", newline="") as csv_file:
        return read_csv_file(csv_file)


def read_csv_file(csv_file):
    rows = []
    reader = csv.DictReader(csv_file, delimiter=";")
    fieldnames = set(reader.fieldnames or [])
    missing_columns = REQUIRED_COLUMNS - fieldnames

    if missing_columns:
        missing = ", ".join(sorted(missing_columns))
        raise CommandError(f"Missing required CSV columns: {missing}")

    for row in reader:
        if not row.get("code"):
            continue

        rows.append(
            {
                "category": row["category"].strip(),
                "code": row["code"].strip(),
                "description": row["description"].strip(),
                "country_code": row["country_code"].strip(),
                "source": row["source"].strip(),
            }
        )

    return rows


def import_referentiel_rows(rows):
    created_count = 0
    updated_count = 0

    for row in rows:
        _, created = Referentiel.objects.update_or_create(
            category=row["category"],
            country_code=row["country_code"],
            code=row["code"],
            defaults={
                "description": row["description"],
                "source": row["source"],
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    return created_count, updated_count


def import_referentiel_from_path(path):
    total_created = 0
    total_updated = 0
    csv_paths = get_csv_paths(path)

    if not csv_paths:
        raise CommandError(f"No CSV files found in: {path}")

    for csv_path in csv_paths:
        created_count, updated_count = import_referentiel_rows(read_csv(csv_path))
        total_created += created_count
        total_updated += updated_count

    return total_created, total_updated, len(csv_paths)


def export_referentiel_to_path(path):
    dump_path = get_dump_path(path)
    referentiels = Referentiel.objects.order_by("category", "country_code", "code")

    with dump_path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=REFERENTIEL_COLUMNS, delimiter=";")
        writer.writeheader()

        for referentiel in referentiels:
            writer.writerow(
                {
                    "category": referentiel.category,
                    "code": referentiel.code,
                    "description": referentiel.description,
                    "country_code": referentiel.country_code or "",
                    "source": referentiel.source or "",
                }
            )

    return dump_path, referentiels.count()
