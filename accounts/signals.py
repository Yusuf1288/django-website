from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    UserProfile.objects.get_or_create(user=instance)
    # No need to save instance.userprofile here as get_or_create 
    # automatically saves the object if it's newly created

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    # Add a check here to prevent error if userprofile does not exist
    if hasattr(instance, 'userprofile'):
        instance.userprofile.save()
