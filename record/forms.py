from django import forms
from collection.models import Collection, Location
from .models import Artist, Record


class RecordForm(forms.ModelForm):
    """ form: RecordForm
    convert location and artist to input fields with autocomplete
    using the following attributes to stop the browser
    showing its own autocomplete field over the top.
    `'autocomplete': 'off'` and `'inputmode': 'search'`.
    then uses the `clean(self)` function to create a new Artist if required.
    """
    # Setup form fields that need to be in a different format
    artist_name = forms.CharField(
        label="Artist",
        widget=forms.TextInput(attrs={
            'class': 'autocomplete',  # required for JS to pick up input field
            'data-url': '/record/artist-autocomplete',  # API endpoint
            'data-target': '#id_artist_id',
            'autocomplete': 'off',
            'inputmode': 'search',
        }))
    artist_id = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    location_name = forms.CharField(
        label="Location",
        widget=forms.TextInput(attrs={
            'class': 'autocomplete',
            'data-url': '/collection/location-autocomplete',  # API endpoint
            'data-target': '#id_location_id',
            'autocomplete': 'off',
            'inputmode': 'search',
        }), required=False)
    location_id = forms.IntegerField(
        widget=forms.HiddenInput(),
        required=False)

    collection = forms.ModelChoiceField(queryset=Collection.objects.none())

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        collection_id = kwargs.pop('collection_id', None)
        super().__init__(*args, **kwargs)
        # limit choices to users own collections
        self.fields['collection'].empty_label = "Please select..."
        self.fields['collection'].queryset = Collection.objects.filter(
            username__user=user)
        # get current selected collection, if it exists
        if collection_id:
            # get the current collection from kwargs
            self.fields['collection'].initial = collection_id
        # If this form is pre-filled, get current values
        if kwargs.get('instance'):
            # get the current artist/location
            self.fields['artist_name'].initial = self.instance.artist
            self.fields['location_name'].initial = self.instance.location
        if not user.my_profile.premium:
            self.fields['image'].disabled = True
            self.fields['hide_record'].disabled = True
            self.fields['image'].help_text = "Premium Feature."
            self.fields['hide_record'].help_text = "Premium Feature."

    class Meta:
        """
        Don't include the slug field in the form as it is auto created on save
        """
        model = Record
        fields = ['artist_name', 'artist_id', 'a_side', 'b_side', 'image',
                  'large_hole', 'hide_record', 'notes', 'location_name',
                  'location_id', 'collection'
                  ]
        labels = {'hide_record': 'Hide this record from public view'}

    def clean(self):
        """
        Returns a valid artist.
        Creates a new artist if one doesn't exist
        modified 12/12/25 SDThornes
        Also returns location.
        Error if ID not found
        """
        cleaned = super().clean()
        artist_id = cleaned.get("artist_id")
        artist_name = cleaned.get("artist_name")
        location_id = cleaned.get("location_id")
        location_name = cleaned.get("location_name")

        if artist_id:
            # If choice from autocomplete
            try:
                cleaned["artist"] = Artist.objects.get(id=artist_id)
            except Artist.DoesNotExist:
                self.add_error("artist_name", "Artist ID not found.")
        else:
            # If user typed a new name
            if artist_name:
                artist, created = Artist.objects.get_or_create(
                    name=artist_name)
                cleaned["artist"] = artist

        if location_id:
            # If chosen from autocomplete
            try:
                cleaned["location"] = Location.objects.get(id=location_id)
            except Location.DoesNotExist:
                self.add_error("location_name", "Location ID not found.")
        else:
            # If user typed a new location
            if location_name:
                location, created = Location.objects.get_or_create(
                    name=location_name)
                cleaned["location"] = location

        return cleaned
