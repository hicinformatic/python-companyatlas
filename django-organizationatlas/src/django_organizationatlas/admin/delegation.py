from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel

from ..models.delegation import OrganizationAtlasDelegation
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE


class OrganizationAtlasDelegationInline(admin.TabularInline):
    model = OrganizationAtlasDelegation
    fk_name = "organization"
    extra = 1
    fields = ["delegation", "valid_from", "valid_to", "source", "country_code"]
    raw_id_fields = ["delegation"]


@admin.register(OrganizationAtlasDelegation)
class OrganizationAtlasDelegationAdmin(AdminBoostModel):
    list_display = ["organization", "delegation", "valid_from", "valid_to", "created_at"]
    list_filter = ["valid_from", "valid_to", "source", "country_code", "created_at"]
    search_fields = [
        "organization__denomination",
        "organization__code",
        "delegation__denomination",
        "delegation__code",
    ]
    readonly_fields = ["created_at", "updated_at"]
    raw_id_fields = ["organization", "delegation"]

    def change_fieldsets(self):
        self.add_to_fieldset(None, ["organization", "delegation", "valid_from", "valid_to"])
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)
