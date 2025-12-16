# forms.py
from django import forms
from .models import My_Profile


class ProfileForm(forms.ModelForm):
    """ Allows user to change their displayname """
    class Meta:
        model = My_Profile
        fields = ['name']


class FullProfileForm(forms.ModelForm):
    """ all order fields relating to profile """
    class Meta:
        model = My_Profile
        fields = [
            'default_phone_number',
            'default_street_address1',
            'default_street_address2',
            'default_town_or_city',
            'default_county',
            'default_postcode',
            'default_country',
        ]
