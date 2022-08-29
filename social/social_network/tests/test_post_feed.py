from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from social_network.models import Post

UserModel = get_user_model()

class FeedTest(TestCase):
    fixtures = [
        "posts.fixture.json",
        "users.fixture.json",
    ]

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        password1 = "userpasswd"
        password2 = "user1passwd"
        cls.user1: UserModel = UserModel.objects.create_user(username="user1", password=password1)
        cls.user2: UserModel = UserModel.objects.create_user(username="user2", password=password2)
        cls.password1 = password1
        cls.password2 = password2

        cls.ann_password = "psswrd1234"
        cls.ann = UserModel.objects.get(username="Ann")

    def test_feed_access(self):
        """
        test feed access
        """

        # unauthorized user access test
        response = self.client.get(
            reverse("social_network:feed", kwargs={"pk": self.user1.pk})
        )

        self.assertEqual(response.status_code, 302)
        url = reverse("login") + f"?next=" + f"/feed/{self.user1.pk}/"
        self.assertURLEqual(
            response.url,
            url
        )

        # authorized user access test
        self.client.login(username=self.user2.username, password=self.password2)
        response = self.client.get(
            reverse("social_network:feed", kwargs={"pk": self.user1.pk})
        )

        self.assertEqual(response.status_code, 403)

        # feed owner access test
        self.client.login(username=self.user1.username, password=self.password1)
        response = self.client.get(
            reverse("social_network:feed", kwargs={"pk": self.user1.pk})
        )

        self.assertEqual(response.status_code, 200)

    def test_feed(self):
        """
        test feed
        """
        self.client.login(username=self.ann.username, password=self.ann_password)
        response = self.client.get(
            reverse("social_network:feed", kwargs={"pk": self.ann.pk})
        )

        self.assertEqual(response.status_code, 200)

        # only friends posts included test
        friends = [friend.user for friend in self.ann.friends.all()]
        posts_list = Post.objects.filter(user__in=friends)
        posts_in_context = response.context["post_list"]
        self.assertEqual(len(posts_list), len(posts_in_context))
        for post1, post2 in zip(posts_list, posts_in_context):
            self.assertEqual(post1.pk, post2.pk)
