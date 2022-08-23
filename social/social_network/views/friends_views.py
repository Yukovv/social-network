from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest
from django.shortcuts import redirect
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView

from social_network.models import FriendRequest, FriendList
from social_authorization.models import UserModel


class AddToFriendView(LoginRequiredMixin, View):
    """
    View to send a friend request.
    """
    def post(self, request: HttpRequest, receiver_pk):
        receiver = UserModel.objects.get(pk=receiver_pk)
        friend_request = FriendRequest.objects.filter(receiver=receiver, sender=request.user).first()
        if (
                request.user not in receiver.friends.all()
                and not friend_request
        ):
            friend_request = FriendRequest.create(receiver=receiver, sender=request.user)
        elif friend_request:
            friend_request.is_active = True
            friend_request.save()

        return redirect(reverse("social_network:profile", kwargs={"pk": receiver_pk}))


class AcceptFriendRequestView(LoginRequiredMixin, View):
    """
    View to accept a friend request.
    """
    def post(self, request: HttpRequest, friend_request_pk):
        friend_request = FriendRequest.objects.get(pk=friend_request_pk)
        friend_request.accept()
        return redirect(reverse("social_network:friend_requests", kwargs={"pk": request.user.pk}))


class DeclineFriendRequestView(LoginRequiredMixin, View):
    """
    View to decline a friend request.
    """
    def post(self, request: HttpRequest, friend_request_pk):
        friend_request = FriendRequest.objects.get(pk=friend_request_pk)
        friend_request.decline()
        return redirect(reverse("social_network:friend_requests", kwargs={"pk": request.user.pk}))


class RemoveFromFriendsView(LoginRequiredMixin, View):
    """
    View to remove user from the friend list.
    """
    def post(self, request: HttpRequest, user_to_remove_pk):
        friend_list = FriendList.objects.get(user=request.user)
        user_to_remove = UserModel.objects.get(pk=user_to_remove_pk)
        friend_list.end_friendship(some_user=user_to_remove)

        return redirect(request.META.get("HTTP_REFERER"))


class FriendRequestsView(LoginRequiredMixin, ListView):
    """
    List of received friend requests.
    """
    def get_queryset(self):
        queryset = FriendRequest.objects.filter(receiver=self.request.user, is_active=True).select_related('sender')
        return queryset

    template_name = 'social_network/friend_requests.html'


class FriendListView(LoginRequiredMixin, DetailView):
    """
    List of user's friends.
    """
    queryset = FriendList.objects.prefetch_related('friends')

    template_name = 'social_network/friend_list.html'