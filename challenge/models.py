from django.db import models
from core.models import TimeStampModel
from django.core.validators import MaxValueValidator, FileExtensionValidator
import os


class Challenge(TimeStampModel):
    FREQUENCY = (
        ("주 1일", 1),
        ("주 2일", 2),
        ("주 3일", 3),
        ("주 4일", 4),
        ("주 5일", 5),
        ("주 6일", 6),
        ("주 7일", 7),
        ("평일 매일", 8),
        ("주말 매일", 9),
    )
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
    frequency = models.CharField(max_length=50, choices=FREQUENCY, default="")
    duration = models.CharField(max_length=50, choices=DURATIONS, null=True)
    certifications = models.ManyToManyField(
        "Certification", related_name="challenge_certifications", blank=True, default=""
    )
    start_time = models.CharField(max_length=30, default="", blank=True)
    end_time = models.CharField(max_length=30, default="", blank=True)
    notice = models.TextField(blank=True)
    # photo_example = models.ManyToManyField("SuccessPhotoExample", default="")
    member = models.ManyToManyField(
        "user.Profile",
        through="ChallengeApply",
        related_name="challenge_apply",
    )
    max_member = models.IntegerField(default=1, validators=[MaxValueValidator(20)])
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


class PhotoExample(models.Model):
    challenge_name = models.ForeignKey(
        "Challenge",
        related_name="photo_example_challenge",
        verbose_name="challenge name",
        on_delete=models.CASCADE,
        null=True,
    )
    photo = models.ImageField(
        upload_to=upload_to_certi_photo_example,
        height_field=None,
        width_field=None,
        max_length=None,
        blank=True,
        null=True,
    )
    TYPE = (
        (0, "success"),
        (1, "fail"),
    )
    type = models.CharField(max_length=50, choices=TYPE, default="")
    owner = models.ForeignKey(
        "user.User",
        verbose_name="owner",
        on_delete=models.CASCADE,
        related_name="photo_owner",
        default="",
        null=True,
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
