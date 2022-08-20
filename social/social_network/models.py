from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

from social_authorization.models import UserModel


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, max_length=2000)
    img = models.ImageField(null=True, upload_to='images/posts', )
    likes = models.ManyToManyField(UserModel)
    time = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, related_name="posts")

    def __str__(self):
        return self.title


class Dialogue(models.Model):
    members = models.ManyToManyField(UserModel)

    # def __str__(self):
    #     return "".join(self.members)


class Message(models.Model):
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name="message")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.text
