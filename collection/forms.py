from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):

    class Meta:
        fields = ['name']
        model = Collection
