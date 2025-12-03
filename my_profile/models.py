from django.db import models
from django.contrib.auth.models import User


class My_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, unique=True)
    premium = models.BooleanField(default=False)
    sub_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "User Profile"
