from django.contrib.auth import get_user_model
from django.db import models

from social_authorization.models import UserModel


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, max_length=2000)
    img = models.ImageField(null=True, upload_to='images/posts')
    likes = models.ManyToManyField(UserModel)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, related_name="posts")

    def __str__(self):
        return self.title