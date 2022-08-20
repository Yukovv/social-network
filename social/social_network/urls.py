from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    UserListView,
    UserProfileView,
    DialogueView,
    DialoguesListView,
    PostCreateView,
    start_page,
)

app_name = "social_network"

urlpatterns = [
    path('', start_page, name="start_page"),
    path('users/', UserListView.as_view(), name="users"),
    path('profile/<int:pk>/', UserProfileView.as_view(), name="profile"),
    path('create_post/', PostCreateView.as_view(), name="create_post"),
    path('<int:pk>/dialogues/', DialoguesListView.as_view(), name="dialogues_list"),
    path('dialogues/<int:dialogue_pk>/', DialogueView.as_view(), name="dialogue"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
