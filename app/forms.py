from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.forms import ModelForm
from app.models import Recension, User, Party, PartyPosters
from bootstrap_datepicker_plus.widgets import DatePickerInput, DateTimePickerInput


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
        fields = ['username', 'first_name', 'last_name', 'date_of_birth',
                  'gender', 'avatar_url', 'password1', 'password2']


class PartyForm(ModelForm):
    party_poster_fk = forms.ModelChoiceField(
        queryset=PartyPosters.objects.all(),
        empty_label=None,
    )

    class Meta:
        model = Party
        fields = ['title', 'total_allowed_guest', 'description', 'starts_at',
                  'closed_at', 'location', 'party_poster_fk']
        widgets = {
            'starts_at': DateTimePickerInput(),
            'closed_at': DateTimePickerInput()
        }


class RecensionForm(ModelForm):
    class Meta:
        model = Recension
        fields = ['text', 'rating']
