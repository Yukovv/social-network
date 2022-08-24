from django.urls import path

from .views import UserCreationView, LogoutView, LoginView, activate


urlpatterns = [
    path('register/', UserCreationView.as_view(), name="register"),
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate")
]
