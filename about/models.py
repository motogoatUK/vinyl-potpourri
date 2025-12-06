from django.db import models


class About(models.Model):
    """
    Stores about us text.
    """
    title = models.CharField(max_length=50, unique=True)
    content = models.TextField()
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
