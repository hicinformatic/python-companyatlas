from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.data import OrganizationAtlasData
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE


@admin.register(OrganizationAtlasData)
class OrganizationAtlasDataAdmin(AdminBoostModel):
    list_display = ["organization", "data_type", "value", "resolved_referentiel", "created_at"]
    list_filter = ["data_type", "country_code", "created_at"]
    search_fields = ["organization__denomination", "data_type", "value"]
    readonly_fields = ["resolved_referentiel", "created_at", "updated_at"]
    raw_id_fields = ["organization"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_resolved_referentiel()

    def resolved_referentiel(self, obj):
        return format_data_referentiel(obj)
    resolved_referentiel.short_description = _("Referentiel")
    resolved_referentiel.admin_order_field = "sql_resolved_referentiel_description"

    def change_fieldsets(self):
        self.add_to_fieldset(None, ("organization", "data_type", "value_type", "value", "resolved_referentiel"))
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)


class OrganizationAtlasDataInline(admin.TabularInline):
    model = OrganizationAtlasData
    extra = 1
    fields = ["data_type", "value_type", "value", "resolved_referentiel", "source", "country_code"]
    readonly_fields = ["resolved_referentiel"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_resolved_referentiel()

    def resolved_referentiel(self, obj):
        return format_data_referentiel(obj)
    resolved_referentiel.short_description = _("Referentiel")


def format_data_referentiel(obj):
    referentiel_id = getattr(obj, "sql_resolved_referentiel_id", None)
    description = getattr(obj, "sql_resolved_referentiel_description", None)

    if not referentiel_id or not description:
        return "-"

    url = reverse(
        "admin:django_organizationatlas_organizationatlasreferentiel_change",
        args=[referentiel_id],
    )
    return format_html('<a href="{}">{}</a>', url, description)
