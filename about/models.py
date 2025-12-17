from django.db import models


class About(models.Model):
    """
    Stores about us text and optional image
    """
    title = models.CharField(max_length=50, unique=True)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)
    free_tier_records = models.PositiveSmallIntegerField(default=10)

    def __str__(self):
        return self.title
