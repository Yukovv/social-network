from django.db import models
from django.utils import timezone

from social_network.models import UserModel


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