from django import forms
from .models import Client, Organization, Sector, Status

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "position", "email", "phone_number", "gender", "organization"]

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = ["organization_name", "type_of_organization", "country_of_operation", "organization_size", "revenue_size", "website_url", "social_media", "history"]

class SectorForm(forms.ModelForm):
    class Meta:
        model = Sector
        fields = ["sector"]

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["status"]
