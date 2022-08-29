from django.test import TestCase
from django.urls import reverse

from social_authorization.models import UserModel
from social_network.models import Post, Comment


class PostDeleteTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        password1 = "userpasswd"
        password2 = "user1passwd"
        cls.user1: UserModel = UserModel.objects.create_user(username="user1", password=password1)
        cls.user2: UserModel = UserModel.objects.create_user(username="user2", password=password2)
        cls.password1 = password1
        cls.password2 = password2
        cls.post_data = {"title": "ttl", "body": "body"}
        cls.post = Post.objects.create(title="ttl", body="body", user=cls.user1)

    def test_post_delete_access(self):
        """
        test post delete access
        """

        # unauthorized user access test
        response = self.client.get(
            reverse('social_network:post_delete', kwargs={"pk": self.post.pk}),
        )

        self.assertEqual(response.status_code, 302)
        url = reverse("login") + f"?next=" + f"/posts/{self.post.pk}/delete-post/"

        self.assertURLEqual(
            response.url,
            url
        )

        # authorized user access test
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get(
            reverse('social_network:post_delete', kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(response.status_code, 403)

        # post author access test
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get(
            reverse('social_network:post_delete', kwargs={"pk": self.post.pk}),
        )
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        """
        test post delete
        """
        self.client.login(username=self.user1.username, password=self.password1)

        response = self.client.post(
            reverse('social_network:post_delete', kwargs={"pk": self.post.pk}),
        )

        self.assertEqual(response.status_code, 302)
        self.assertURLEqual(
            response.url,
            reverse("social_network:profile", kwargs={"pk": self.user1.pk})
        )

        # test post doesn't exist anymore
        post = Post.objects.filter(title=self.post_data["title"]).first()
        self.assertIsNone(post)
