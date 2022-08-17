from django.urls import path

from .views import UserCreationView, LogoutView, LoginView


urlpatterns = [
    path('register/', UserCreationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
]