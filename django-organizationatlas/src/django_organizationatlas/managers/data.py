from django.db import models
from django.db.models import OuterRef, Subquery

from ..models.referentiel import OrganizationAtlasReferentiel


class OrganizationAtlasDataQuerySet(models.QuerySet):
    def with_resolved_referentiel(self):
        referentiel = OrganizationAtlasReferentiel.objects.filter(
            category=OuterRef("data_type"),
            country_code=OuterRef("country_code"),
            code=OuterRef("value"),
        )
        return self.annotate(
            sql_resolved_referentiel_id=Subquery(referentiel.values("pk")[:1]),
            sql_resolved_referentiel_description=Subquery(
                referentiel.values("description")[:1]
            ),
        )

    def with_referentiel_description(self):
        return self.with_resolved_referentiel()


class OrganizationAtlasDataManager(models.Manager):
    def get_queryset(self):
        return OrganizationAtlasDataQuerySet(self.model, using=self._db)

    def with_resolved_referentiel(self):
        return self.get_queryset().with_resolved_referentiel()

    def with_referentiel_description(self):
        return self.get_queryset().with_referentiel_description()
