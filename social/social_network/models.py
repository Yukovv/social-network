from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from PIL import Image

UserModel = get_user_model()


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
        """
        Add user to likes.
        """
        self.likes.add(some_user)
        self.save()
        
    def remove_like(self, some_user: UserModel):
        """
        Remove user from likes.
        """
        self.likes.remove(some_user)
        self.save()

    def get_likes(self):
        """
        Return a list of users eho liked the post.
        """
        return [user for user in self.likes.all()]
        

class Dialogue(models.Model):
    members = models.ManyToManyField(UserModel)
    
    @classmethod
    def create(cls, *users: UserModel):
        dialogue = cls()
        dialogue.save()
        for user in users:
            dialogue.members.add(user)
        return dialogue    


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

    def __str__(self):
        return self.user.username

    def add_friend(self, some_user: UserModel):
        if some_user not in self.friends.all():
            self.friends.add(some_user)
            self.save()

    def remove_friend(self, some_user: UserModel):
        if some_user in self.friends.all():
            self.friends.remove(some_user)
            self.save()

    def end_friendship(self, some_user: UserModel):
         self.remove_friend(some_user)
         
         some_user_friend_list = FriendList.objects.get(user=some_user)
         some_user_friend_list.remove_friend(self.user)


class FriendRequest(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="sender")
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="receiver")
    is_active = models.BooleanField(blank=True, null=False, default=True)

    def accept(self):
        """
        add receiver to sender friends list and vice versa
        """
        receiver_friend_list = FriendList.objects.get(user=self.receiver)
        receiver_friend_list.add_friend(self.sender)

        sender_friend_list = FriendList.objects.get(user=self.sender)
        sender_friend_list.add_friend(self.receiver)

        self.is_active = False
        self.save()

    def decline(self):
        """
        decline a friend request
        set 'is_active' to False
        """
        self.is_active = False
        self.save()

    @classmethod
    def create(cls, receiver, sender):
        friend_request = cls(receiver=receiver, sender=sender)
        friend_request.save()
        return friend_request 