# forms.py

from django import forms
from .models import User

class RegistrationForm(forms.Form):
    new_username = forms.CharField(max_length=50, required=True)
    new_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_picture']