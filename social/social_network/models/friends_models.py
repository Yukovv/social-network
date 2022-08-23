from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


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