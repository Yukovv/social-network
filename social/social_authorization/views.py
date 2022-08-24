from django.http import HttpRequest
from django.shortcuts import redirect, render, resolve_url
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LogoutView as LogoutViewGeneric,
    LoginView as LoginViewGeneric,
)

from social.settings import BASE_DIR, LOGIN_REDIRECT_URL
from .forms import UserCreationForm


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


class LoginView(LoginViewGeneric):
    template_name = "social_authorization/login.html"

    def get_default_redirect_url(self):
        """Return the default redirect URL."""
        if self.next_page:
            return resolve_url(self.next_page)
        else:
            return resolve_url(LOGIN_REDIRECT_URL + str(self.request.user.pk))


class LogoutView(LogoutViewGeneric):
    next_page = reverse_lazy("login")
