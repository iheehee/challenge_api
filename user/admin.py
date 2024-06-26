from django.contrib import admin

# from django.contrib.auth.admin import UserAdmin
from . import models


@admin.register(models.User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        "email",
        "level",
        "nickname_id",
    )


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("id", "nickname", "avatar")
