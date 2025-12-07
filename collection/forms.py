from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'description']
        model = Collection
        labels = {
            'name': 'Collection Name:',
            'description': 'Description (max 120 characters):'
            }
        widgets = {
            'description': forms.TextInput(
                attrs={'placeholder': '[OPTIONAL]'}
                ),
        }
