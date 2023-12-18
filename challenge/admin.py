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
