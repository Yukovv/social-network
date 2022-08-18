from django.contrib import admin

from .models import UserProfile


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birthday')


admin.site.register(UserProfile, ProfileAdmin)