from django.contrib import admin

from .models import Dialogue, Message, Post


admin.site.register(Dialogue)
admin.site.register(Message)
admin.site.register(Post)
