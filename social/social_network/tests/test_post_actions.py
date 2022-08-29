from django.test import TestCase
from django.urls import reverse

from social_authorization.models import UserModel
from social_network.models import Post, Comment


class PostCreationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        password = "userpasswd"
        cls.user: UserModel = UserModel.objects.create_user(username="user", password=password)
        cls.password = password
        cls.post = Post.objects.create(title="ttl", body="body", user=cls.user)
        cls.comment_data = {"text": "some comment"}

    def test_like(self):
        """
        test adding and removing like
        """
        self.client.login(username=self.user.username, password=self.password)

        # add like
        response = self.client.post(
            reverse('social_network:like', kwargs={"post_pk": self.post.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(self.user in self.post.likes.all())
        self.assertURLEqual(
            response.url,
            reverse("social_network:profile", kwargs={"pk": self.user.pk})
        )

        # remove like
        response = self.client.post(
            reverse('social_network:like', kwargs={"post_pk": self.post.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(self.user in self.post.likes.all())
        self.assertURLEqual(
            response.url,
            reverse("social_network:profile", kwargs={"pk": self.user.pk})
        )

    def test_comment(self):
        """
        test add comment
        """
        self.client.login(username=self.user.username, password=self.password)

        response = self.client.post(
            reverse('social_network:comment', kwargs={"post_pk": self.post.pk}),
            data=self.comment_data
        )

        self.assertEqual(response.status_code, 302)

        comment = Comment.objects.get(text=self.comment_data["text"])
        self.assertURLEqual(
            response.url,
            reverse("social_network:profile", kwargs={"pk": self.user.pk})
        )
