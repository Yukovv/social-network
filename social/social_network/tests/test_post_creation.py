from django.test import TestCase
from django.urls import reverse

from social_authorization.models import UserModel
from social_network.models import Post


class PostCreationTest(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        password = "userpasswd"
        cls.user = UserModel.objects.create_user(username="user", password=password)
        cls.password = password
        cls.post_data = {"title": "ttl", "body": "some text"}

    def test_post_creation_access(self):
        response = self.client.get(
            reverse('social_network:create_post')
        )
        self.assertEqual(302, response.status_code)
        self.assertURLEqual(response.url, reverse('login') + '?next=/create_post/')

        self.client.login(username=self.user.username, password=self.password)
        response = self.client.get(reverse('social_network:create_post'))
        self.assertEqual(200, response.status_code)

    def test_post_creation(self):
        self.client.login(username=self.user.username, password=self.password)
        response = self.client.post(
            reverse('social_network:create_post'),
            data=self.post_data
        )

        self.assertEqual(response.status_code, 302)

        post = Post.objects.get(title=self.post_data["title"])
        self.assertURLEqual(
            response.url,
            reverse("social_network:profile", kwargs={"pk": self.user.pk})
        )
