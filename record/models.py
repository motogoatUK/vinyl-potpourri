from django.db import models

# Create your models here.
"""
A single instance of Record relating to collection, artist and location
"""


class Record(models.Model):
    a_side = models.CharField(max_length=80, blank=False, unique=True)
    b_side = models.CharField(max_length=80, blank=True)
    large_hole = models.BooleanField(default=False)
    notes = models.TextField()
    # image = models.ImageField(default='placeholder')
    slug = models.SlugField(max_length=80, unique=True)

    def __str__(self):
        return f'{self.a_side} by {"Artist"}'
