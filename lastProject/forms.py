# forms.py

from django import forms
from .models import UserProfile

class RegistrationForm(forms.Form):
    new_username = forms.CharField(max_length=50, required=True)
    new_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=50, required=True, widget=forms.PasswordInput)

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture']