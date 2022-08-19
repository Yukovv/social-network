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
    success_url = reverse_lazy("social_network:profile")
    form_class = UserCreationForm
    template_name = "social_authorization/register.html"


class LoginView(LoginViewGeneric):
    next_page = reverse_lazy("social_network:profile")

    template_name = "social_authorization/login.html"


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("login")
