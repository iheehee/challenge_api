from django.contrib import admin
from . import models


@admin.register(models.Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "owner",
        "title_banner",
        "summery",
        "description",
        "start_day",
        "notice",
    )


@admin.register(models.ChallengeApply)
class ChallengeApplyAdmin(admin.ModelAdmin):
    list_display = (
        "challenge",
        "user",
        "created",
    )
