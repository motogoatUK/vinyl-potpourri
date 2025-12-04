from django import forms
from collection.models import Collection
from .models import Artist, Record


class RecordForm(forms.ModelForm):
    """ form: RecordForm
    convert location and artist to input fields
    with autocomplete using django-autocomplete-light
    then use create_or_save in view.
    Don't include the slug field
    """
    artist_name = forms.CharField(
        label="Artist",
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "inputmode": "search",
        }))
    artist_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)

    collection = forms.ModelChoiceField(queryset=Collection.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        # limit choices to users own collections
        self.fields['collection'].empty_label = None
        self.fields['collection'].queryset = Collection.objects.filter(
            username__user=user)
        # If this form is pre-filled, get current values
        # get the current collection from kwargs
        this_collection = kwargs['instance'].collection
        self.fields['collection'].initial = this_collection
        # get the current artist using a different way than kwargs
        self.fields['artist_name'].initial = self.instance.artist

    class Meta:
        model = Record
        # don't include 'slug'
        fields = ['artist_name', 'artist_id', 'a_side', 'b_side',
                  'large_hole', 'notes', 'location',
                  'collection'
                  ]
        # include the slug but make it hidden
        # widgets = {
        #     'slug': forms.HiddenInput()
        # }

    def clean(self):
        """
        Returns a valid artist.
        Creates a new artist if one doesn't exist
        """
        cleaned = super().clean()
        artist_id = cleaned.get("artist_id")
        name = cleaned.get("artist_name")

        if artist_id:
            cleaned["artist"] = Artist.objects.get(id=artist_id)
        else:
            # create new artist
            artist, _ = Artist.objects.get_or_create(name=name)
            cleaned["artist"] = artist

        return cleaned
