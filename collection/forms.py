from django import forms
from .models import Collection


class CollectionForm(forms.ModelForm):
    """
    CollectionForm for collection information
    disables image field in not premium user
    """
    def __init__(self, *args, **kwargs):
        userp = kwargs.pop('userp', None)
        super().__init__(*args, **kwargs)
        if not userp:
            self.fields['image'].disabled = True
            self.fields['image'].help_text = "Premium Feature."

    class Meta:
        fields = ['name', 'description', 'image']
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
