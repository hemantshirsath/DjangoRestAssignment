
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Artist

@receiver(post_save, sender=User)
def create_artist_profile(sender, instance, created, **kwargs):
    if created:
        Artist.objects.create(user=instance)
