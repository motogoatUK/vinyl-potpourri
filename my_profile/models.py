from django.db import models
from django.contrib.auth.models import User
from django_countries.fields import CountryField


class My_Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, unique=True)
    premium = models.BooleanField(default=False)
    sub_date = models.DateField(null=True, blank=True)
    exp_date = models.DateField(null=True, blank=True)
    num_records = models.IntegerField(default=0)
    # fields to save stripe customer details
    default_phone_number = models.CharField(
        max_length=20, null=True, blank=True)
    default_street_address1 = models.CharField(
        max_length=80, null=True, blank=True)
    default_street_address2 = models.CharField(
        max_length=80, null=True, blank=True)
    default_town_or_city = models.CharField(
        max_length=40, null=True, blank=True)
    default_county = models.CharField(max_length=80, null=True, blank=True)
    default_postcode = models.CharField(
        max_length=20, null=True, blank=True)
    default_country = CountryField(
        blank_label='Country', null=True, blank=True)

    def __str__(self):
        return f"{self.user}"

    class Meta:
        verbose_name = "User Profile"
