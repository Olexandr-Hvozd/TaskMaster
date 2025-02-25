from django.contrib import admin

from .models import User, Quit


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "username", "email", "is_superuser", "password")
    list_display_links = ("id", "username", "email")
    list_per_page = 15
    search_fields = ["username", "email", "is_superuser"]
    list_filter = ["username", "email"]


@admin.register(Quit)
class QuitAdmin(admin.ModelAdmin):
    list_display = ("id", "text", "author")
    list_display_links = ("id", "text", "author")
    list_per_page = 15
    search_fields = ["text", "author"]
    list_filter = ["text", "author"]
