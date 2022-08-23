from django.contrib import admin

from .models import Dialogue, Message, Post, FriendRequest, FriendList


class PostAdmin(admin.ModelAdmin):
    fields = ['id', 'user', 'title', 'body', 'likes']
    list_display = ('id', 'user', 'title', 'body', 'get_likes')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('user').prefetch_related('likes')


class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver', 'sender', 'is_active')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('receiver', 'sender')


admin.site.register(Dialogue)
admin.site.register(Message)
admin.site.register(Post, PostAdmin)
admin.site.register(FriendList)
admin.site.register(FriendRequest, FriendRequestAdmin)
