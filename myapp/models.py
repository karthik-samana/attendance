from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields you want
    phone = models.CharField(max_length=14,null=True, blank=True)
    sem=models.CharField(max_length=1,blank=True)
    section=models.CharField(max_length=1,blank=True)
    # Add other fields as needed

    # You can also add methods or properties to this model if needed

# Automatically create a UserProfile instance when a new User is created
from django.db.models.signals import post_save
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.userprofile.save()


class Temp(models.Model):
    longitude=models.CharField(max_length=10,null=True,blank=True)
    latitude=models.CharField(max_length=10,null=True,blank=True)
    