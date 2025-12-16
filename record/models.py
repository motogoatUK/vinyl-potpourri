from django.db import models
from django.db.models import Q
from collection.models import Collection, Location


def get_default_artist():
    """
    get_default_artist returns 'Unknown'
    creates the db record if it doesn't exist
    """
    return Artist.objects.get_or_create(name='Unknown')


class RecordQuerySet(models.QuerySet):
    """
    RecordQuerySet filters the available list of records
    if they are not hidden OR they belong to the requesting user
    """
    def visible(self, user):
        if user.is_authenticated:
            return self.filter(Q(hide_record=False) |
                               Q(collection__username__user=user))
        return self.filter(hide_record=False)


class Record(models.Model):
    """
    A single instance of Record relating to collection, artist and location

    artist references Artist.name by default and is set to Unknown initially
    """
    a_side = models.CharField(max_length=80, blank=False)
    b_side = models.CharField(max_length=80, blank=True)
    large_hole = models.BooleanField(default=False)
    hide_record = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True, blank=True)
    slug = models.SlugField(max_length=80, unique=True)
    artist = models.ForeignKey(
        'Artist',
        to_field='name',
        on_delete=models.SET_DEFAULT,
        default=get_default_artist
    )
    location = models.ForeignKey(
        Location,
        to_field='name',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
    )

    objects = RecordQuerySet.as_manager()

    def __str__(self):
        return f'{self.id}: {self.a_side} by {self.artist}'


class Artist(models.Model):
    """
    Artist object contains artist name
    """
    name = models.CharField(max_length=80, blank=False, unique=True)

    def __str__(self):
        return self.name
