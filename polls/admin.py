from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Client, Organization, Sector, Status


# Inlines
class SectorInline(TabularInline):
    model = Sector
    extra = 1
    tab = True


class StatusInline(TabularInline):
    model = Status
    extra = 1
    tab = True


# Admin Classes
@admin.register(Client)
class ClientAdmin(ModelAdmin):
    inlines = [SectorInline, StatusInline]
    list_display = ("name", "email", "position", "organization")
    search_fields = ("name", "email", "position", "organization__organization_name")
    list_filter = ("gender", "organization__country_of_operation")


@admin.register(Organization)
class OrganizationAdmin(ModelAdmin):
    list_display = ("organization_name", "type_of_organization", "country_of_operation", "organization_size", "revenue_size")
    search_fields = ("organization_name", "type_of_organization", "country_of_operation")
    list_filter = ("type_of_organization", "country_of_operation")


@admin.register(Sector)
class SectorAdmin(ModelAdmin):
    list_display = ("sector", "client")
    list_filter = ("sector",)


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ("status", "time", "client")
    list_filter = ("status",)

