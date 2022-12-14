from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User, BaseUserManager
from django.db.models.signals import post_save
from PIL import Image

from django.dispatch import receiver

from social_network.models import FriendList

UserModel: User = get_user_model()


class EmailUserManager(BaseUserManager):
    """
    User manager for email confirmation.
    """
    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves user with the given password and email.
        """


class UserProfile(models.Model):

    class Gender(models.TextChoices):
        MALE = 'M'
        FEMALE = 'F'
        OTHER = 'O'

    user: UserModel = models.OneToOneField(
        UserModel,
        on_delete=models.CASCADE,
        primary_key=True,
    )

    birthday = models.DateField(null=True, blank=True)
    city = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    bio = models.TextField(max_length=300, blank=True)
    occupation = models.CharField(max_length=50, blank=True)
    avatar = models.ImageField(null=True, upload_to='images/avatars', blank=True)

    def __str__(self):
        return f"{self.user.username} profile"
    

@receiver(post_save, sender=UserProfile)
def image_compressor(instance: UserProfile, **kwargs):
    if instance.avatar:
        with Image.open(instance.avatar.path) as avatar:
            new_avatar = avatar.resize(size=(150, 200))
            new_avatar.save(instance.avatar.path, optimize=True, quality=50)


@receiver(post_save, sender=UserModel)
def user_saved_handler(instance: UserModel, created: bool, **kwargs):
    if not created:
        return

    FriendList.objects.create(user=instance)
    UserProfile.objects.create(user=instance)
