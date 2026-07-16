"""Organization data models."""


from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .organization import OrganizationAtlasOrganization
from .referentiel import OrganizationAtlasReferentiel
from .source import OrganizationAtlasSourceBase
from .temporal import TemporalValidityMixin
from ..managers.data import OrganizationAtlasDataManager


class OrganizationAtlasData(TemporalValidityMixin, OrganizationAtlasSourceBase):
    """Organization data from various backends."""

    temporal_key_fields = ("organization", "source", "country_code", "data_type")

    organization = models.ForeignKey(
        OrganizationAtlasOrganization,
        on_delete=models.CASCADE,
        related_name="to_organizationatlasdata",
        verbose_name=_("Organization"),
        help_text=_("Organization this data belongs to"),
    )
    data_type = models.CharField(
        max_length=100,
        verbose_name=_("Data Type"),
        help_text=_("Type of data (e.g., denomination, siren, capital, employees)"),
    )
    value_type = models.CharField(
        max_length=10,
        verbose_name=_("Value Type"),
        choices=[
            ("str", _("String")),
            ("int", _("Integer")),
            ("float", _("Float")),
            ("json", _("JSON")),
        ],
        default="str",
        help_text=_("Type of the value (str, int, float, json)"),
    )
    value = models.TextField(
        verbose_name=_("Value"),
        help_text=_("Data value"),
    )
    referentiel = models.ManyToManyField(
        OrganizationAtlasReferentiel,
        verbose_name=_("Referentiel"),
        help_text=_("Referentiel this data belongs to"),
        related_name="to_organizationatlasdata",
        blank=True,
    )

    objects = OrganizationAtlasDataManager()

    class Meta:
        verbose_name = _("Organization Data")
        verbose_name_plural = _("Organization Data")
        indexes = [
            models.Index(fields=["organization", "country_code"]),
            models.Index(fields=["data_type"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "source", "country_code", "data_type"],
                condition=Q(valid_to__isnull=True),
                nulls_distinct=False,
                name="unique_open_organizationatlasdata",
            ),
        ]
        ordering = ["data_type", "-created_at"]

    def __str__(self):
        return (
            f"{self.organization.denomination} - {self.source} - "
            f"{self.country_code} - {self.data_type}"
        )

    @property
    def referentiel_description(self):
        if hasattr(self, "sql_referentiel_description"):
            return self.sql_referentiel_description
        first = self.referentiel.values_list("description", flat=True).first()
        return first or ""

    @property
    def resolved_referentiel_description(self):
        if hasattr(self, "sql_resolved_referentiel_description"):
            return self.sql_resolved_referentiel_description or ""

        referentiel = OrganizationAtlasReferentiel.objects.filter(
            category=self.data_type,
            country_code=self.country_code,
            code=self.value,
        ).first()
        return referentiel.description if referentiel else ""
