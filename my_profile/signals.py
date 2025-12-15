from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth.models import User
from .models import My_Profile


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        My_Profile.objects.create(user=instance, name=instance.username)


@receiver(user_logged_in)
def check_premium_expiry(sender, request, user, **kwargs):
    profile = getattr(user, "my_profile", None)
    if not profile or not profile.exp_date:
        return
    today = timezone.now().date()
    premium = profile.exp_date >= today
    # true if exp_date has not passed, false if it has
    if profile.premium != premium:
        profile.premium = premium
        profile.save(update_fields=["premium"])
