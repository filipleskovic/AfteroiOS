from django.contrib.auth.forms import UserCreationForm
from django import forms
from app.models import User
from bootstrap_datepicker_plus.widgets import DatePickerInput

class CustomUserForm(UserCreationForm):
    date_of_birth = forms.DateField(widget=DatePickerInput())
    GENDER_CHOICES = [
        ('muško', 'Muško'),
        ('žensko', 'Žensko'),
    ]
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    avatar_url = forms.CharField(max_length=128, required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'date_of_birth', 'gender', 'avatar_url', 'password1', 'password2']
        