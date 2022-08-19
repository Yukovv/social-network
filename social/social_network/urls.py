from django.urls import path

from .views import (
    UserProfileView,
    start_page,
)

app_name = "social_network"

urlpatterns = [
    path('', start_page, name="start_page"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="profile")
]
