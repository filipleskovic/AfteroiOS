from django.contrib.auth.forms import UserCreationForm
from django import forms
from app.models import User


class CustomUserForm(UserCreationForm):
    date_of_birth = forms.DateTimeField(required=True)
    gender = forms.CharField(max_length=32, required=True)
    avatar_url = forms.CharField(max_length=128, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'avatar_url', 'password1', 'password2']