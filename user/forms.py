from django import forms
from django.forms import ModelForm

from user.models import CustomerProfile, User


class RegisterForm(ModelForm):
    class Meta:
        model = User
        fields = ("fullName", "email", "password")


class RegisterForm_Customer_profile(ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ("phone", "address")


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder": "Enter Your E-mail Address"}),
                             )
    password = forms.CharField(
        max_length=255,
        widget=forms.PasswordInput(
            attrs={"placeholder": "Enter Your Password", "id": "password"}
        ),
    )
