from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from django.dispatch import receiver

UserModel: User = get_user_model()


class UserProfile(models.Model):
    user: UserModel = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    birthday = models.DateField()
    city = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, null=True)
    bio = models.TextField(max_length=300, blank=True)
    occupation = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(null=True, upload_to='images/avatars')

    def __str__(self):
        return f"{self.user.username} profile"


@receiver(post_save, sender=UserModel)
def user_saved_handler(instance: UserModel, created: bool, **kwargs):
    if not created:
        return

    UserProfile.objects.create(user=instance)