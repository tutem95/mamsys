from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "usuarios"

urlpatterns = [
    path("", views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("elegir-empresa/", views.company_select, name="company_select"),
    path("sin-empresa/", views.no_company, name="no_company"),
]

