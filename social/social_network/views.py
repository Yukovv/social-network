from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.template.defaulttags import url
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import UserModel, Post
from social_authorization.models import UserProfile


class UserProfileView(LoginRequiredMixin, DetailView):
    queryset = UserModel.objects.select_related('userprofile')
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
