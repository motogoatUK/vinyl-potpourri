from django import forms
from .models import Record


class RecordForm(forms.ModelForm):
    """ form: RecordForm
    convert location and artist to input fields
    then use create_or_save in view.
    make slug a hidden field
    """

    class Meta:
        model = Record
        exclude = ['slug']
        # fields = '__all__'
        # Hide the slug
        # widgets = {
        #     'slug': forms.HiddenInput()
        # }
