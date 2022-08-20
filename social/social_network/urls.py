from django.urls import path

from .views import (
    UserProfileView,
    DialogueView,
    DialoguesListView,
    PostCreateView,
    start_page,
)

app_name = "social_network"

urlpatterns = [
    path('', start_page, name="start_page"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="profile"),
    path('create_post/', PostCreateView.as_view(), name="create_post"),
    path('<int:pk>/dialogues/', DialoguesListView.as_view(), name="dialogues_list"),
    path('dialogues/<int:dialogue_pk>/', DialogueView.as_view(), name="dialogue"),
]
