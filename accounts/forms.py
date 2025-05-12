from django.contrib.auth.forms import UserCreationForm
from django import forms
from.models import CustomUser

class CustomUserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password1', 'password2']

class UpdateUserDashboardForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'phone_number', 'country', 'address', 'city', 'postal_code', 'address', 'profile_picture']