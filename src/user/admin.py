from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import APIToken, CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "user_type", "is_staff", "is_active")
    fieldsets = UserAdmin.fieldsets + ((None, {"fields": ("user_type",)}),)


@admin.register(APIToken)
class APITokenAdmin(admin.ModelAdmin):
    list_display = ("key", "user", "created", "is_active")
    search_fields = ("key", "user__username")
