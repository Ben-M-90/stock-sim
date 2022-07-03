from pickle import TRUE
from re import U
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm
from .models import CustomUser
from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import _unicode_ci_compare


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=TRUE)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super(CustomUserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('username',)

class CustomPasswordResetForm(PasswordResetForm):
    username = UsernameField(required=TRUE)

    class Meta:
        model = CustomUser
        fields = ("username", "email")

    def get_users(self, email, username):
        email_field_name = CustomUser.get_email_field_name()
        username_field_name = CustomUser.get_username()
        active_users = CustomUser._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
                "s__iexact" % username_field_name: username
                }
            )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )
