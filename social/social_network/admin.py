from django.contrib import admin

from .models import Dialogue, Message, Post, FriendRequest, FriendList

class FriendRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'receiver', 'sender', 'is_active')
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('receiver', 'sender')
    
admin.site.register(Dialogue)
admin.site.register(Message)
admin.site.register(Post)
admin.site.register(FriendList)
admin.site.register(FriendRequest, FriendRequestAdmin)
