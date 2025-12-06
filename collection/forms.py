from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'description']
        model = Collection
        labels = {'description': 'Description (max 120 characters):'}
