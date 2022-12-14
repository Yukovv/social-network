from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone

UserModel = get_user_model()


class Post(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField(blank=True, max_length=2000)
    img = models.ImageField(null=True, upload_to='images/posts', blank=True)
    likes = models.ManyToManyField(UserModel)
    time = models.DateTimeField(default=timezone.now)

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, null=True, related_name="posts")

    class Meta:
        ordering = ['-time']

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


class Comment(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="user_comments")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    text = models.TextField(max_length=500)
    time = models.DateTimeField(default=timezone.now)
