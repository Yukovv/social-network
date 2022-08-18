from django.urls import path

from .views import (
    UserProfileView,
)

app_name = "social_network"

urlpatterns = [
    path('', UserProfileView.as_view(), name="profile")
]
