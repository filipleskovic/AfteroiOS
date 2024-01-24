from django.contrib.auth.forms import UserCreationForm
from django import forms
from app.models import User


class CustomUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']