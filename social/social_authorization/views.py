from django.shortcuts import resolve_url
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LogoutView as LogoutViewGeneric,
    LoginView as LoginViewGeneric,
)

from .forms import UserCreationForm
from .models import UserModel


class UserCreationView(CreateView):
    model = UserModel
    form_class = UserCreationForm
    template_name = "social_authorization/register.html"

    def get_success_url(self):
        return reverse(self.next_page, kwargs={"pk": self.request.user.pk})


class LoginView(LoginViewGeneric):
    next_page = "social_network:profile"
    template_name = "social_authorization/login.html"

    def get_success_url(self):
        return reverse(self.next_page, kwargs={"pk": self.request.user.pk})




class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("login")
