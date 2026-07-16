from django.db import models
from django.utils.translation import gettext_lazy as _

from ..managers.referentiel import OrganizationAtlasReferentielManager
from .source import OrganizationAtlasSourceBase


class OrganizationAtlasReferentiel(OrganizationAtlasSourceBase):
    """Referentiel model - parent model for referentiel data."""
    category = models.CharField(
        max_length=255,
        verbose_name=_("Name"),
        help_text=_("Referentiel name"),
    )
    code = models.CharField(
        max_length=255,
        verbose_name=_("Code"),
        help_text=_("Referentiel code"),
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Description"),
        help_text=_("Referentiel description"),
    )
    characteristics = models.TextField(
        blank=True,
        default="",
        verbose_name=_("Characteristics"),
        help_text=_("Referentiel characteristics"),
    )
    priority = models.IntegerField(
        verbose_name=_("Priority"),
        help_text=_("Referentiel priority"),
        default=0,
    )
    usage_type = models.CharField(
        max_length=100,
        verbose_name=_("Usage Type"),
        help_text=_("Usage type"),
        choices=[
            ("description", _("Description")),
            ("configuration", _("Configuration")),
            ("characteristics", _("Characteristics")),
        ],
        default="description",
    )

    objects = OrganizationAtlasReferentielManager()

    class Meta:
        verbose_name = _("Referentiel")
        verbose_name_plural = _("Referentiels")
        ordering = ["-priority", "category", "code"]
        indexes = [
            models.Index(fields=["category"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["category", "country_code", "code"],
                name="unique_referentiel_country_code",
            ),
        ]

    @property
    def used_count(self):
        return self.sql_used_count
