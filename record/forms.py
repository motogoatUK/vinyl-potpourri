from django import forms
from collection.models import Collection
from .models import Record


class RecordForm(forms.ModelForm):
    """ form: RecordForm
    convert location and artist to input fields
    then use create_or_save in view.
    make slug a hidden field
    """
    collection = forms.ModelChoiceField(queryset=Collection.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # get the current collection
        this_collection = kwargs['instance'].collection
        # limit choices to users own collections
        self.fields['collection'].empty_label = None
        self.fields['collection'].queryset = Collection.objects.filter(
            username__user=user)
        # pre-select the current collection
        self.fields['collection'].initial = this_collection

    class Meta:
        model = Record
        # don't include 'slug'
        fields = ['artist', 'a_side', 'b_side',
                  'large_hole', 'notes', 'location',
                  'collection'
                  ]
        # include the slug but make it hidden
        # widgets = {
        #     'slug': forms.HiddenInput()
        # }
