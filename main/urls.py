# users/urls.py
from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("register/", views.register_request, name="register"),
    path("login/", views.login_request, name="login"),
    path("logout/", views.logout_request, name="logout"),
    path("password_reset/", views.password_reset_request, name="password_reset"),
    path('stock_details/<str:ticker>', views.stock_details, name="stock_details"),
    path('profile/<str:username>', views.profile, name="profile"),
    path('profile_settings/', views.profile_settings, name="profile_settings"),
]
