from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from .models import UserModel, Post, Dialogue as DialogueModel, FriendRequest, FriendList
from .forms import MessageForm, PostCreationForm
from social_authorization.models import UserProfile


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


class DialoguesListView(LoginRequiredMixin, View):
    """
    List of users dialogues.
    """
    def get(self, request: HttpRequest, pk):
        dialogues = DialogueModel.objects.filter(members__in=[request.user.pk]).prefetch_related('members')
        context = {
            "user": request.user,
            "dialogues": dialogues,
        }
        return render(request, 'social_network/dialogues.html', context)


class DialogueView(LoginRequiredMixin, View):
    """
    Dialogue view.
    Show previous and send a new messages.
    """
    def get(self, request: HttpRequest, dialogue_pk):
        dialogue = get_object_or_404(DialogueModel.objects.prefetch_related('members'), id=dialogue_pk)
        if request.user not in dialogue.members.all():
            return render(request, "403.html")

        context = {
            "messages": dialogue.message.all(),
            "form": MessageForm()
        }
        return render(request, "social_network/dialogue.html", context)

    def post(self, request: HttpRequest, dialogue_pk):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.dialogue_id = dialogue_pk
            message.user = request.user
            message.save()

        return redirect(reverse("social_network:dialogue", kwargs={"dialogue_pk": dialogue_pk}))


class PostCreateView(LoginRequiredMixin, CreateView):
    """
    View to create a post.
    """
    model = Post
    form_class = PostCreationForm
    template_name = "social_network/post_creation.html"

    def get_success_url(self):
        return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})

    def form_valid(self, form):
        self.object: Post = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)
    

class PostDeleteView(UserPassesTestMixin, DeleteView):
    """
    View to delete a post.
    """
    queryset = Post.objects.select_related("user")
    template_name = "social_network/post_confirm_delete.html"

    def test_func(self):
        post = Post.objects.get(pk=self.kwargs["pk"])
        return post.user.pk == self.request.user.pk

    def get_success_url(self):
        return reverse("social_network:profile", kwargs={"pk": self.request.user.pk})


class AddToFriendView(LoginRequiredMixin, View):
    """
    View to send a friend request.
    """
    def post(self, request: HttpRequest, receiver_pk):
        receiver = UserModel.objects.get(pk=receiver_pk)
        friend_request = FriendRequest.objects.get(receiver=receiver, sender=request.user)
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
