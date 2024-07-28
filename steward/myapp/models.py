from django.db import models
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import AbstractUser
from django.conf import settings



class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (1, 'Worker'),
        (2, 'Steward'),
        (3, 'Organization'),
    )
    user_type = models.PositiveSmallIntegerField(choices=USER_TYPE_CHOICES)

User = get_user_model()

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name

class WorkAddress(models.Model):
    address = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    def __str__(self):
        return self.address

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True)
    work_address = models.ForeignKey(WorkAddress, on_delete=models.SET_NULL, null=True, blank=True)
    is_profile_complete = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username

class Feedback(models.Model):
    FEEDBACK_CHOICES = [
        ('feedback', 'Feedback'),
        ('recognition', 'Recognition'),
        ('grievance', 'Grievance'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    work_address = models.ForeignKey(WorkAddress, on_delete=models.CASCADE)
    feedback_type = models.CharField(max_length=20, choices=FEEDBACK_CHOICES, default='feedback')
    content = models.TextField()
    private = models.BooleanField(default=False)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user.username if self.user else 'Anonymous'}"

class CommunityEntry(models.Model):
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} - {self.content[:20]}"

class WorkJournalEntry(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.title

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()
