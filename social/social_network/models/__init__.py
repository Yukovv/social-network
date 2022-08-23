from django.contrib.auth import get_user_model

from dialogue_models import Dialogue, Message
from friends_models import FriendRequest, FriendList
from post_models import Post


UserModel = get_user_model()
