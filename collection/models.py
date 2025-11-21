from django.db import models
from django.contrib.auth.models import User


class Collection(models.Model):
    """
    A single instance of Collection relating to username and location

    """
    name = models.TextField(max_length=80, blank=False, null=True, unique=True)
    username = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )


class Location(models.Model):
    """
    A collection must have a location
    A location can exist without a collection
    """
    name = models.TextField(max_length=100, unique=True,)
    collection = models.ForeignKey(
        Collection,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        )
