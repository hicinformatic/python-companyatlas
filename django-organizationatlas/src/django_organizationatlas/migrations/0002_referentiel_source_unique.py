from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("django_organizationatlas", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="organizationatlasreferentiel",
            name="code",
            field=models.CharField(
                help_text="Referentiel code",
                max_length=255,
                verbose_name="Code",
            ),
        ),
        migrations.AddConstraint(
            model_name="organizationatlasreferentiel",
            constraint=models.UniqueConstraint(
                fields=("category", "country_code", "source", "code"),
                name="unique_referentiel_source_code",
            ),
        ),
    ]
