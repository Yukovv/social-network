from django.http import HttpRequest
from django.shortcuts import resolve_url, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LogoutView as LogoutViewGeneric,
    LoginView as LoginViewGeneric,
)

from .forms import UserCreationForm
from .models import UserModel


class UserCreationView(CreateView):
    """
    Registration view.
    """
    def get(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm()

        return render(request, "social_authorization/register.html", {"form": form})

    def post(self, request: HttpRequest, *args, **kwargs):
        form = UserCreationForm(data=request.POST)
        if form.is_valid():
            user = form.save()

            return redirect(reverse("social_network:profile_settings", kwargs={"pk": user.pk}))

        return render(request, "social_authorization/register.html", {"form": form})
    # model = UserModel
    # form_class = UserCreationForm
    # template_name = "social_authorization/register.html"
    #
    # def get_success_url(self):
    #     return reverse("social_network:profile_settings", kwargs={"pk": self.request.user.pk})


class LoginView(LoginViewGeneric):
    next_page = "social_network:profile"
    template_name = "social_authorization/login.html"

    def get_success_url(self):
        return reverse(self.next_page, kwargs={"pk": self.request.user.pk})


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("login")
