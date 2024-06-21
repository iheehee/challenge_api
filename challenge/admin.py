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

    )


""" @admin.register(models.ChallengeApply)
class ChallengeApplyAdmin(admin.ModelAdmin):
    list_display = (
        "challenge_id",
        "user",
        "created",
    ) """


@admin.register(models.Certification)
class Certification(admin.ModelAdmin):
    list_display = (
        "id",
        "challenge_id",
        "user_profile_id",
        "certification_num",
        "certification_date",
        "certification_photo",
        "certification_local_photo_url",
        "certification_dairy",
        
    )


