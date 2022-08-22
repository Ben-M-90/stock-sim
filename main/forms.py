from multiprocessing import Value
from pickle import TRUE
from re import U
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordResetForm, PasswordChangeForm
from .models import CustomUser, UserProfile, StockPortfolio, Trade
from django import forms
from django.contrib.auth.forms import UsernameField
from django.contrib.auth.forms import _unicode_ci_compare
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal


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
            and _unicode_ci_compare(email, getattr(u, email_field_name)))

class NewPortfolioForm(forms.ModelForm):
    class Meta:
        model = StockPortfolio
        fields = ('name', 'start_balance', 'description')

class BuyStockForm(forms.ModelForm):
    class Meta:
        model = Trade
        fields = ('quantity', 'portfolio',)
        
        def __init__(self, user, *args, **kwargs):
            super(BuyStockForm, self).__init__(*args, **kwargs)
            portfolio_names = StockPortfolio.objects.filter(user=user)
            self.widgets = {'portfolio': forms.ModelChoiceField(queryset=portfolio_names)}

class SellStockForm(forms.ModelForm):
    sell_quantity = forms.DecimalField(initial = 0, validators=[MinValueValidator(round(Decimal(0.001), 3))])

    class Meta:
        model = Trade
        fields = ('quantity',)
        widgets = {'quantity': forms.HiddenInput()}

class PortfolioForm(forms.ModelForm):
    class Meta:
        model = StockPortfolio
        fields = ('name', 'description')
        widgets = {'description': forms.Textarea(attrs={'cols':40, 'rows':3})}

#class ChangeBalanceForm(forms.ModelForm):
#    class Meta:
#        model = StockPortfolio
#        fields = ('balance',)

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('tagline', 'about_me', 'user_timezone')

    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args,**kwargs)
        self.fields['tagline'].required = False
        self.fields['about_me'].required = False

class ProfilePictureForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('profile_picture', 'cover_image',)

class ProfileCoverImageForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('cover_image',)

class EditUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name')

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'autofocus': False})