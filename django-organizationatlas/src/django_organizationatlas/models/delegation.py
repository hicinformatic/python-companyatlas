from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q
from django.utils.translation import gettext_lazy as _

from .source import OrganizationAtlasSourceBase
from .temporal import TemporalValidityMixin


class OrganizationAtlasDelegation(TemporalValidityMixin, OrganizationAtlasSourceBase):
    """Delegation of authority from one organization to another."""

    temporal_key_fields = ("organization", "delegation")

    organization = models.ForeignKey(
        "django_organizationatlas.OrganizationAtlasOrganization",
        on_delete=models.CASCADE,
        related_name="delegations_given",
        verbose_name=_("From Organization"),
        help_text=_("Organization that grants the delegation"),
    )
    delegation = models.ForeignKey(
        "django_organizationatlas.OrganizationAtlasOrganization",
        on_delete=models.CASCADE,
        related_name="delegations_received",
        verbose_name=_("To Organization"),
        help_text=_("Organization that receives the delegation"),
    )

    class Meta:
        verbose_name = _("Delegation")
        verbose_name_plural = _("Delegations")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["organization", "delegation"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["organization", "delegation"],
                condition=Q(valid_to__isnull=True),
                name="unique_open_organization_delegation",
            ),
        ]

    def clean(self):
        super().clean()
        if self.organization_id and self.organization_id == self.delegation_id:
            raise ValidationError(
                {"delegation": _("An organization cannot delegate to itself.")}
            )

    def __str__(self):
        return f"{self.organization} → {self.delegation}"
