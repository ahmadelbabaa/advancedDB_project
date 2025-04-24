from django.urls import path
from . import views
from .views import public_form_view, home_view

urlpatterns = [
    path("", home_view, name="home"),
    path("", views.index, name="index"),
    path("relationshipsystem/", views.relationship_system_view, name="relationship_system"),
    path("form/", public_form_view, name="form"),
]

