from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpRequest
from django.shortcuts import redirect, render, resolve_url
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.generic import CreateView
from django.contrib.auth.views import (
    LogoutView as LogoutViewGeneric,
    LoginView as LoginViewGeneric,
)
from django.core.mail import EmailMessage

from social.settings import LOGIN_REDIRECT_URL
from .forms import UserCreationForm
from .tokens import account_activation_token

UserModel = get_user_model()


def activate(request: HttpRequest, uidb64, token):
    """
    Activate user account.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel.objects.get(pk=uid)
    except:
        user = None

    if user and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        login(request, user)

        messages.success(
            request,
            "Thank you for your email confirmation. Now you can update your profile information, if you want."
        )
        return redirect(reverse("social_network:profile_settings", kwargs={"pk": request.user.pk}))

    else:
        messages.error(request, "Activation link is invalid!")

    return redirect(reverse('login'))


def activate_email(request: HttpRequest, user: UserModel, to_email):
    """
    Send confirmation letter to new user email.
    """
    mail_subject = "Activate your user account."
    message = render_to_string(
        'social_authorization/activate_user_account.html',
        {
            "user": user.username,
            "domain": get_current_site(request).domain,
            "uid": urlsafe_base64_encode(force_bytes(user.pk)),
            "token": account_activation_token.make_token(user),
            "protocol": "https" if request.is_secure() else "http"
        }
    )
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"Hello, {user}! Please, confirm your email to activate the account.")
    else:
        messages.error(request, f"Problem sending email to {to_email}, check if you type it correctly.")


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
            user: UserModel = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, form.cleaned_data.get('email'))

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
