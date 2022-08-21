from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from PIL import Image

from social_authorization.models import UserModel


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, max_length=2000)
    img = models.ImageField(null=True, upload_to='images/posts', blank=True)
    likes = models.ManyToManyField(UserModel)
    time = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, related_name="posts")

    def __str__(self):
        return self.title
    
    def add_like(self, some_user: UserModel):
        self.likes.add(some_user)
        
    def remove_like(self, some_user: UserModel):    
        self.likes.remove(some_user)
        

class Dialogue(models.Model):
    members = models.ManyToManyField(UserModel)


class Message(models.Model):
    dialogue = models.ForeignKey(Dialogue, on_delete=models.CASCADE, related_name="message")
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    text = models.TextField(max_length=400)
    time = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['time']

    def __str__(self):
        return self.text


class FriendList(models.Model):
    user = models.OneToOneField(
        UserModel,
        primary_key=True,
        on_delete=models.CASCADE,
        related_name="user"
    )
    friends = models.ManyToManyField(UserModel, blank=True, related_name="friends")

    def add_friend(self, some_user: UserModel):
        if some_user not in self.friends:
            self.friends.add(some_user)

    def remove_friend(self, some_user: UserModel):
        if some_user in self.friends:
            self.friends.remove(some_user)

    def end_friendship(self, some_user: UserModel):
         self.friends.remove_friend(some_user)
         
         some_user_friend_list = FriendList.objects.get(user=some_user)
         some_user_friend_list.remove_friend(self.user)

