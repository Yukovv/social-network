from django.http import HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserModel, Post, Dialogue as DialogueModel
from .forms import MessageForm, PostCreationForm
from social_authorization.models import UserProfile


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = UserModel.objects.select_related('userprofile').prefetch_related('posts')
    template_name = "social_network/profile.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["user_posts"] = Post.objects.filter(user=self.object).prefetch_related('likes')
        return context


def start_page(request: HttpRequest):
    if request.user.is_authenticated:
        return render(request, "social_network/profile.html")
    else:
        return redirect(reverse('login'))


class UserListView(LoginRequiredMixin, ListView):
    queryset = UserModel.objects.filter(is_staff=False)
    template_name = "social_network/users.html"


class DialoguesListView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, pk):
        dialogues = DialogueModel.objects.filter(members__in=[request.user.pk]).prefetch_related('members')
        context = {
            "user": request.user,
            "dialogues": dialogues,
        }
        return render(request, 'social_network/dialogues.html', context)


class DialogueView(LoginRequiredMixin, View):
    def get(self, request: HttpRequest, dialogue_pk):
        dialogue = get_object_or_404(DialogueModel.objects.prefetch_related('members'), id=dialogue_pk)
        if request.user not in dialogue.members.all():
            return render(request, "403.html")

        context = {
            "messages": dialogue.message.all(),
            "form": MessageForm()
        }
        return render(request, "social_network/dialogue.html", context, )

    def post(self, request: HttpRequest, dialogue_pk):
        form = MessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.dialogue_id = dialogue_pk
            message.user = request.user
            message.save()

        return redirect(reverse("social_network:dialogue", kwargs={"dialogue_pk": dialogue_pk}))


class PostCreateView(LoginRequiredMixin, CreateView):
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