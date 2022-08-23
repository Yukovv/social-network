from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic import DetailView, ListView, UpdateView
from django.views.generic.edit import BaseUpdateView

from social_network.forms import ProfileForm
from social_network.models import Post, Dialogue as DialogueModel, FriendRequest
from social_authorization.models import UserModel, UserProfile


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
        friend_request_1 = FriendRequest.objects.filter(sender=self.request.user, receiver=self.object).first()
        friend_request_2 = FriendRequest.objects.filter(sender=self.object, receiver=self.request.user).first()
        if (
            self.request.user.pk == self.object.pk
            or self.request.user in [friend.user for friend in self.object.friends.all()]
            or (friend_request_1 and friend_request_1.is_active)
            or (friend_request_2 and friend_request_2.is_active)
        ):
            is_add_friend_btn = False

        context["is_add_friend_btn"] = is_add_friend_btn

        return context


class ProfileSettingsView(UserPassesTestMixin, UpdateView):
    """
    View to change profile info
    """
    def get(self, request: HttpRequest, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        return render(request, "social_network/profile_settings.html", {"form": ProfileForm(instance=profile)})

    def post(self, request: HttpRequest, *args, **kwargs):
        profile = get_object_or_404(UserProfile, user=request.user)
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        print(form)
        print(form.is_valid())
        print(form.__dict__)

        if form.is_valid():
            form.save()
            return redirect(reverse("social_network:profile", kwargs={"pk": request.user.pk}))

        return render(request, "social_network/profile_settings.html", {"form": ProfileForm(instance=profile)})

    # model = UserProfile
    # form_class = ProfileForm
    # template_name = "social_network/profile_settings.html"
    #
    # def get_success_url(self):
    #     return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})
    #
    # def post(self, request, *args, **kwargs):
    #     form = ProfileForm(request.POST, request.FILES)
    #     form.save()
    #
    #     return redirect(reverse("social_network:profile", kwargs={"pk": request.user.pk}))

    def test_func(self):
        return self.request.user.pk == self.kwargs["pk"]


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