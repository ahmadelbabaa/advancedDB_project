from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline
from .models import Client, Company, Interest, Status


class InterestInline(TabularInline):
    model = Interest
    extra = 1
    tab=True


class StatusInline(TabularInline):
    model = Status
    extra = 1
    tab=True


@admin.register(Client)
class ClientAdmin(ModelAdmin):
    inlines = [InterestInline, StatusInline]
    list_display = ("name", "email", "position", "company")
    search_fields = ("name", "email", "position", "company__company_name")
    list_filter = ("gender", "company__region")


@admin.register(Company)
class CompanyAdmin(ModelAdmin):
    list_display = ("company_name", "region", "country", "company_size", "revenue_size")
    search_fields = ("company_name", "region", "country")
    list_filter = ("region", "country")


@admin.register(Interest)
class InterestAdmin(ModelAdmin):
    list_display = ("interest_name", "client")


@admin.register(Status)
class StatusAdmin(ModelAdmin):
    list_display = ("status", "time")
    list_filter = ("status",)
