from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Patient, Appointment


class SignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=1, max_value=120, required=True)
    contact = forms.CharField(max_length=15, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'age', 'contact', 'password1', 'password2']


class AppointmentForm(forms.ModelForm):
    date_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        input_formats=['%Y-%m-%dT%H:%M'],
    )

    class Meta:
        model = Appointment
        fields = ['date_time']
