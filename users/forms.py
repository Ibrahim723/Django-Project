# users/forms.py
from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(max_length=255)
    balance = forms.FloatField()
