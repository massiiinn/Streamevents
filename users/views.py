from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from .forms import CustomUserCreationForm, CustomAuthenticationForm, CustomUserUpdateForm

User = get_user_model()


def home_view(request):
    return render(request, "home.html")


def register_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Ja has iniciat sessió.")
        return redirect("users:profile")

    form = CustomUserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, f"Compte creat correctament. Benvingut/da, {user.username}!")
        return redirect("users:profile")

    return render(request, "registration/register.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        messages.info(request, "Ja estàs autenticat.")
        return redirect("users:profile")

    form = CustomAuthenticationForm(request, data=request.POST or None)
    if form.is_valid():
        user = form.get_user()
        login(request, user)
        messages.success(request, f"Benvingut/da, {user.username}!")
        return redirect("users:profile")

    return render(request, "registration/login.html", {"form": form})


@login_required
def logout_view(request):
    logout(request)
    messages.info(request, "Has tancat la sessió correctament.")
    return redirect("users:login")


@login_required
def profile_view(request):
    return render(request, "users/profile.html", {"user": request.user})


@login_required
def edit_profile_view(request):
    form = CustomUserUpdateForm(request.POST or None, request.FILES or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Perfil actualitzat correctament.")
        return redirect("users:profile")
    return render(request, "users/edit_profile.html", {"form": form})


def public_profile_view(request, username):
    user = get_object_or_404(User, username=username)
    return render(request, "users/public_profile.html", {"profile_user": user})

def password_reset_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        if not username or not new_password or not confirm_password:
            messages.error(request, "Omple tots els camps.")
        elif new_password != confirm_password:
            messages.error(request, "Les contrasenyes no coincideixen.")
        else:
            try:
                user = User.objects.get(username=username)
                user.set_password(new_password)
                user.save()
                messages.success(request, "Contrasenya restablerta correctament. Ja pots iniciar sessió.")
                return redirect("users:login")
            except User.DoesNotExist:
                messages.error(request, "No existeix cap usuari amb aquest nom d'usuari.")

    return render(request, "registration/password_reset.html")

