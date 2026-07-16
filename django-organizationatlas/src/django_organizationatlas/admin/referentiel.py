from io import TextIOWrapper

from django.contrib import admin
from django.contrib import messages
from django.core.management.base import CommandError
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django_boosted import AdminBoostModel
from django_boosted.decorators import admin_boost_view

from ..forms.referentiel import ReferentielImportForm
from ..models.referentiel import OrganizationAtlasReferentiel
from ..models.source import ORGANIZATIONATLAS_FIELDS_SOURCE
from ..services.referentiel import import_referentiel_rows, read_csv_file

base_fields = [
    "category",
    "usage_type",
    "code",
    "description",
    "characteristics",
    "priority",
    "used_count",
]

source_fields = [
    "country_code",
    "source",
    "created_at",
    "updated_at",
]


@admin.register(OrganizationAtlasReferentiel)
class OrganizationAtlasReferentielAdmin(AdminBoostModel):
    list_display = [*base_fields, *source_fields]
    list_filter = ["category", "usage_type", "country_code", "source"]
    search_fields = [
        "category",
        "code",
        "description",
        "characteristics",
        "country_code",
        "source",
    ]
    readonly_fields = ["created_at", "updated_at", "used_count"]

    def get_queryset(self, request):
        return super().get_queryset(request).with_usage_count()

    def used_count(self, obj):
        return getattr(obj, "sql_used_count", "—")
    used_count.short_description = _("Used count")
    used_count.admin_order_field = "sql_used_count"

    @admin_boost_view(
        "form",
        _("Import referentiel"),
        path_fragment="import-referentiel",
        requires_object=False,
        permission="change",
    )
    def import_referentiel(self, request):
        if not self.has_change_permission(request):
            messages.error(request, _("You do not have permission to import referentiel data."))
            return redirect(self._get_changelist_url())

        form = ReferentielImportForm(request.POST or None, request.FILES or None)

        if request.method == "POST" and form.is_valid():
            uploaded_file = form.cleaned_data["csv_file"]

            try:
                with TextIOWrapper(uploaded_file.file, encoding="utf-8") as text_file:
                    rows = read_csv_file(text_file)
                created_count, updated_count = import_referentiel_rows(rows)
            except UnicodeDecodeError:
                messages.error(request, _("CSV file must be encoded in UTF-8."))
            except CommandError as error:
                messages.error(request, str(error))
            else:
                messages.success(
                    request,
                    _("Imported %(created)s created and %(updated)s updated referentiel rows.")
                    % {"created": created_count, "updated": updated_count},
                )
                return redirect(self._get_changelist_url())

        return {
            "form": form,
            "buttons": {"_import": _("Import")},
        }

    def _get_changelist_url(self):
        opts = self.model._meta
        return reverse(
            f"admin:{opts.app_label}_{opts.model_name}_changelist",
            current_app=self.admin_site.name,
        )

    def change_fieldsets(self):
        self.add_to_fieldset(None, base_fields)
        self.add_to_fieldset(_("Source"), ORGANIZATIONATLAS_FIELDS_SOURCE)
