from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    start_page,
    UserProfileView,
    UserListView,
    FriendRequestsView,
    FriendListView,
    AddToFriendView,
    RemoveFromFriendsView,
    AcceptFriendRequestView,
    DeclineFriendRequestView,
    PostCreateView,
    PostDeleteView,
    LikeView,
    FeedView,
    DialogueView,
    DialoguesListView,
)

app_name = "social_network"

urlpatterns = [
    path('', start_page, name="start_page"),
    
    path('profile/<int:pk>/', UserProfileView.as_view(), name="profile"),
    
    path('users/', UserListView.as_view(), name="users"),
    
    # friends views
    path('<int:pk>/friend_requests/', FriendRequestsView.as_view(), name="friend_requests"),
    path('<int:pk>/friend_list/', FriendListView.as_view(), name="friend_list"),
    path('add_friend/<int:receiver_pk>/', AddToFriendView.as_view(), name="add_friend"),
    path('accept_friend/<int:friend_request_pk>/', AcceptFriendRequestView.as_view(), name="accept_friend"),
    path('decline_friend/<int:friend_request_pk>/', DeclineFriendRequestView.as_view(), name="decline_friend"),
    path('remove_friend/<int:user_to_remove_pk>/', RemoveFromFriendsView.as_view(), name='remove_friend'),
    
    # post views
    path('posts/<int:pk>/delete-post/', PostDeleteView.as_view(), name="post_delete"),
    path('create_post/', PostCreateView.as_view(), name="create_post"),
    path('like_post/<int:post_pk>/', LikeView.as_view(), name="like"),
    path('feed/<int:pk>/', FeedView.as_view(), name="feed"),

    # dialogue views
    path('<int:pk>/dialogues/', DialoguesListView.as_view(), name="dialogues_list"),
    path('dialogues/<int:dialogue_pk>/', DialogueView.as_view(), name="dialogue"),
    
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
