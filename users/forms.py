from django import forms
from django.contrib.auth import get_user_model, password_validation, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.validators import UnicodeUsernameValidator

User = get_user_model()
username_validator = UnicodeUsernameValidator()


class CustomUserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label=_("Contrasenya"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": _("Introdueix la teva contrasenya"),
            "class": "form-control"
        }),
    )
    password2 = forms.CharField(
        label=_("Confirma la contrasenya"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "autocomplete": "new-password",
            "placeholder": _("Repeteix la contrasenya"),
            "class": "form-control"
        }),
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Nom d'usuari")
            }),
            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": _("Correu electrònic")
            }),
            "first_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Nom")
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": _("Cognoms")
            }),
        }

    def clean_username(self):
        username = self.cleaned_data.get("username", "")
        username_validator(username)

        try:
            User.objects.get(username=username)
            raise ValidationError(_("Aquest nom d'usuari ja està registrat."))
        except User.DoesNotExist:
            return username

    def clean_email(self):
        email = self.cleaned_data.get("email", "").lower()
        try:
            User.objects.get(email=email)
            raise ValidationError(_("Aquest email ja està registrat."))
        except User.DoesNotExist:
            return email

    def clean_password2(self):
        pw1 = self.cleaned_data.get("password1")
        pw2 = self.cleaned_data.get("password2")
        if not pw1 or not pw2:
            raise ValidationError(_("Introdueix la contrasenya i la seva confirmació."))
        if pw1 != pw2:
            raise ValidationError(_("Les contrasenyes no coincideixen."))
        password_validation.validate_password(pw1, self.instance)
        return pw2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class CustomUserUpdateForm(forms.ModelForm):
    bio = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            "rows": 4,
            "class": "form-control",
            "placeholder": _("Explica una mica sobre tu...")
        })
    )
    avatar = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "display_name", "bio", "avatar")
        widgets = {
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"}),
            "display_name": forms.TextInput(attrs={"class": "form-control"}),
        }


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label=_("Usuari o correu"),
        widget=forms.TextInput(attrs={
            "autofocus": True,
            "placeholder": _("Nom d'usuari o correu electrònic"),
            "class": "form-control"
        })
    )
    password = forms.CharField(
        label=_("Contrasenya"),
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": _("Introdueix la teva contrasenya"),
            "class": "form-control"
        })
    )

    def clean(self):
        username_or_email = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")

        if username_or_email and password:
            user = authenticate(self.request, username=username_or_email, password=password)
            if not user and "@" in username_or_email:
                try:
                    u = User.objects.get(email__iexact=username_or_email)
                    user = authenticate(self.request, username=u.get_username(), password=password)
                except User.DoesNotExist:
                    user = None

            if user is None:
                raise ValidationError(_("Nom d'usuari o contrasenya incorrectes."), code='invalid_login')

            self.user_cache = user
            self.confirm_login_allowed(user)

        return self.cleaned_data
