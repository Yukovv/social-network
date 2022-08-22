from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import DetailView, ListView

from social.social_network.models import UserModel, Post, Dialogue as DialogueModel, FriendRequest


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = UserModel.objects.select_related('userprofile').prefetch_related('posts')
    template_name = "social_network/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_posts"] = Post.objects.filter(user=self.object).prefetch_related('likes')

        # load dialogue with a profile's owner or create it
        dialogues = DialogueModel.objects.filter(members__in=[self.request.user.pk]).filter(members__in=[self.object.pk])
        if not dialogues:
            dialogue = DialogueModel.create(self.request.user, self.object)
            dialogues = [dialogue]
        elif self.request.user.pk == self.object.pk:
            dialogues = [None]
        context["dialogue"] = dialogues[0]

        # is_add_friend_btn var for 'add to friends' button in the template
        is_add_friend_btn = True
        # friend request from user1 to user2 and from user2 to user1
        friend_request_1 = FriendRequest.objects.filter(sender=self.request.user, receiver=self.object)
        friend_request_2 = FriendRequest.objects.filter(sender=self.object, receiver=self.request.user)
        if (
            self.request.user.pk == self.object.pk
            or self.request.user in self.object.friends.all()
            or (friend_request_1 and friend_request_1[0].is_active)
            or (friend_request_2 and friend_request_2[0].is_active)
        ):
            is_add_friend_btn = False
        print(FriendRequest.objects.filter(sender=self.request.user, receiver=self.object))
        context["is_add_friend_btn"] = is_add_friend_btn

        return context


def start_page(request: HttpRequest):
    """
    View to redirect from the root to profile or authorization
    """
    if request.user.is_authenticated:
        return render(request, "social_network/profile.html")
    else:
        return redirect(reverse('login'))


class UserListView(LoginRequiredMixin, ListView):
    """
    List of all users.
    """
    queryset = UserModel.objects.filter(is_staff=False)
    template_name = "social_network/users.html"