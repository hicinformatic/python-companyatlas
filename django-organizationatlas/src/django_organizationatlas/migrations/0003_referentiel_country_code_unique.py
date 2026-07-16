from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_organizationatlas", "0002_referentiel_source_unique"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="organizationatlasreferentiel",
            name="unique_referentiel_source_code",
        ),
        migrations.AddConstraint(
            model_name="organizationatlasreferentiel",
            constraint=models.UniqueConstraint(
                fields=("category", "country_code", "code"),
                name="unique_referentiel_country_code",
            ),
        ),
    ]
