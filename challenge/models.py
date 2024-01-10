from django.db import models
from core.models import TimeStampModel
from django.core.validators import MaxValueValidator, FileExtensionValidator
import os


class Challenge(TimeStampModel):
    DURATIONS = (
        ("1주 동안", 1),
        ("2주 동안", 2),
        ("3주 동안", 3),
        ("4주 동안", 4),
    )
    title = models.CharField(max_length=140, default="", blank=True)
    owner = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="user", null=True
    )
    title_banner = models.ImageField(
        upload_to="title_banner", default="", blank=True, null=True
    )
    summery = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    start_day = models.DateField(null=True)
    duration = models.CharField(max_length=50, choices=DURATIONS, null=True)
    certifications = models.ManyToManyField(
        "Certification", related_name="challenge_certifications", blank=True, default=""
    )
    start_time = models.CharField(max_length=30, default="", blank=True)
    end_time = models.CharField(max_length=30, default="", blank=True)
    notice = models.TextField(blank=True)
    member = models.ManyToManyField(
        "user.Profile",
        through="ChallengeApply",
        related_name="challenge_apply",
    )
    max_member = models.IntegerField(default=1)
    number_of_applied_member = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title


def upload_to_certi_photo_example(instance, file_name):
    return os.path.join(
        instance.owner.email,
        instance.challenge_name.title,
        "photo_ex",
        file_name,
    )


class ChallengeApply(models.Model):
    applied_id = models.AutoField(primary_key=True)
    challenge = models.ForeignKey(
        "Challenge",
        verbose_name="challenge name",
        on_delete=models.CASCADE,
        related_name="challenge_name",
        default="",
    )
    user = models.ForeignKey(
        "user.Profile",
        verbose_name="member name",
        on_delete=models.CASCADE,
        related_name="member_name",
        default="",
    )
    created = models.DateTimeField(auto_now=True)


class Certification(models.Model):
    certification_id = models.AutoField(primary_key=True)
    challenge = models.ForeignKey(
        "Challenge",
        verbose_name="challenge name",
        on_delete=models.CASCADE,
        related_name="certification_challenge",
        default="",
    )
    user = models.ForeignKey(
        "user.Profile",
        verbose_name="member name",
        on_delete=models.CASCADE,
        related_name="certification_profile",
        default="",
    )
    certification_date = models.DateTimeField(auto_now=True)
    certification_photo = models.FileField(
        upload_to="certification", blank=True, default="", null=True
    )
    certification_comment = models.CharField(max_length=255, blank=True)
