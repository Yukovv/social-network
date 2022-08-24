from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import UserProfile, UserModel


class UserAdmin(BaseUserAdmin):
    model = UserModel
    list_display = ("is_active", "username", "email", "first_name", "last_name", "is_staff")


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'birthday')


admin.site.register(UserProfile, ProfileAdmin)
admin.site.unregister(UserModel)
admin.site.register(UserModel, UserAdmin)
