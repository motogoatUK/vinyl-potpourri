# forms.py
from django import forms
from .models import My_Profile


class ProfileForm(forms.ModelForm):
    """ Allows user to change their displayname """
    class Meta:
        model = My_Profile
        fields = ['name']


class FullProfileForm(forms.ModelForm):
    model = My_Profile
