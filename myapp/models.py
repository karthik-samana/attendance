from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    SECTION_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D','D')
    ]
    SEM_CHOICES=[
        ('1','1'),('2','2'),('3','3'),('4','4'),('5','5'),('6','6'),('7','7'),('8','8')
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # Add additional fields you want
    phone = models.CharField(max_length=14,null=True, blank=True)
    sem=models.CharField(max_length=1,choices=SEM_CHOICES,blank=True)
    section = models.CharField(max_length=1, choices=SECTION_CHOICES)

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
    code=models.CharField(max_length=10,null=True,blank=True)
    expire=models.DateTimeField(auto_now_add=True,null=True,blank=True)
    
class Class(models.Model):
    faculty = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    date = models.DateField()
    code=models.CharField(max_length=10,null=True,blank=True)
    class_id=models.CharField(max_length=10,null=True,blank=True)
    # Your existing Class model fields

class Attendance(models.Model):
    student = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    class_attended = models.ForeignKey(Class, on_delete=models.CASCADE)
    status = models.BooleanField()  # True for present, False for absent
    timestamp = models.DateTimeField(auto_now_add=True)

    