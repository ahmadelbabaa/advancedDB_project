from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Client, Company, Interest

@admin.register(Client)
class ClientAdminClass(ModelAdmin):
    pass

@admin.register(Company)
class CompanyAdminClass(ModelAdmin):
    pass

@admin.register(Interest)
class InterestAdminClass(ModelAdmin):
    pass