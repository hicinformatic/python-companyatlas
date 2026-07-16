from django.contrib import admin
from django.shortcuts import redirect
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel, admin_boost_view

from ..models.organization import ORGANIZATIONATLAS_FIELDS_COMPANY, OrganizationAtlasOrganization
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE
from .address import OrganizationAtlasAddressInline
from .data import OrganizationAtlasDataInline
from .delegation import OrganizationAtlasDelegationInline


@admin.register(OrganizationAtlasOrganization)
class OrganizationAtlasOrganizationAdmin(AdminBoostModel):
    list_display = ["denomination", "code", "headquarters_address_display", "created_at"]
    list_filter = ["created_at"]
    search_fields = ["denomination", "code", "to_organizationatlasdata__value"]
    readonly_fields = ["named_id", "created_at", "updated_at"]
    inlines = [
        OrganizationAtlasDataInline,
        OrganizationAtlasAddressInline,
        OrganizationAtlasDelegationInline,
    ]
    changeform_actions = {
        "refresh_person": _("Refresh Persons"),
        "refresh_address": _("Refresh Addresses"),
        "refresh_data": _("Refresh Data"),
        "refresh_event": _("Refresh Events"),
        "refresh_document": _("Refresh Documents"),
        "full_refresh": _("Full Refresh"),
    }

    def get_queryset(self, request):
        return super().get_queryset(request).with_headquarters()

    def get_search_results(self, request, queryset, search_term):
        queryset, use_distinct = super().get_search_results(request, queryset, search_term)
        return queryset.distinct(), use_distinct

    def change_fieldsets(self):
        self.add_to_fieldset(None, ORGANIZATIONATLAS_FIELDS_COMPANY)
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)

    def headquarters_address_display(self, obj: OrganizationAtlasOrganization) -> str:
        prefetched = getattr(obj, "prefetched_headquarters", None)
        if prefetched:
            return str(prefetched[0].address)
        return "-"
    headquarters_address_display.short_description = _("Headquarters Address")

    def handle_refresh_person(self, request, object_id):
        pass

    @admin_boost_view("message", _("Search Organization"))
    def search_organization(self, request):
        return redirect("admin:django_organizationatlas_organizationatlasvirtualorganization_changelist")
