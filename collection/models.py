from django.db import models
from my_profile.models import My_Profile


class Collection(models.Model):
    """
    A single instance of Collection relating to username and location

    """
    name = models.CharField(max_length=60, blank=False, null=True, unique=True)
    username = models.ForeignKey(
        My_Profile,
        on_delete=models.CASCADE
    )
    description = models.TextField(max_length=120, blank=True, null=True)
    image = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.name


class Location(models.Model):
    """
    A collection must have a location
    A location can exist without a collection
    """
    name = models.TextField(max_length=100, unique=True,)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        )

    def __str__(self):
        return self.name
