from django.db import models

# Create your models here.
"""
A single instance of Record relating to collection, artist and location

artist references Artist.name by default and is set to Unknown initially
"""


def get_default_artist():
    return Artist.objects.get_or_create(name='Unknown')


class Record(models.Model):
    a_side = models.CharField(max_length=80, blank=False, unique=True)
    b_side = models.CharField(max_length=80, blank=True)
    large_hole = models.BooleanField(default=False)
    notes = models.TextField(null=True, blank=True)
    # image = models.ImageField(default='placeholder')
    slug = models.SlugField(max_length=80, unique=True)
    artist = models.ForeignKey(
        'Artist',
        to_field='name',
        on_delete=models.SET_DEFAULT,
        default=get_default_artist
    )

    def __str__(self):
        return f'{self.a_side} by {self.artist}'


class Artist(models.Model):
    name = models.CharField(max_length=80, blank=False, unique=True)
    # image = models.ImageField(default='placeholder') #  for future use

    def __str__(self):
        return self.name
