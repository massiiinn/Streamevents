from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("register/", views.register_view, name="register"),
    path("logout/", views.logout_view, name="logout"),

    path("profile/", views.profile_view, name="profile"),
    path("edit_profile/", views.edit_profile_view, name="edit_profile"),

    path(
        "password_reset/",
        views.password_reset_view,
        name="password_reset"
    ),

    path("<str:username>/", views.public_profile_view, name="public_profile"),
]
