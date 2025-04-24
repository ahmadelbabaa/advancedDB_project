from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from polls import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("admin/", admin.site.urls),
    path("relationshipsystem/", views.relationship_system_view, name="relationship_system"),
    path("login/", auth_views.LoginView.as_view(template_name="polls/login.html"), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page='https://otabr.pythonanywhere.com/'), name="logout"),
    path("form/", views.public_client_form, name="public_form"),
]
