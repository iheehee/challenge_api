from django.db import models
from core.models import TimeStampModel
from django.core.validators import MaxValueValidator, FileExtensionValidator
import os


class Challenge(TimeStampModel):
    
    title = models.CharField(max_length=140, default="", blank=True)
    owner = models.ForeignKey(
        "user.User", on_delete=models.CASCADE, related_name="user", null=True
    )
    title_banner = models.ImageField(
        upload_to="title_banner", default="", blank=True, null=True
    )
    summery = models.CharField(max_length=255, blank=True)
    certifications = models.ManyToManyField(
        "Certification", related_name="challenge_certifications", blank=True, default=""
    )
    certifications_count = models.IntegerField(default=0)
    is_opened = models.BooleanField(default=False)
    max_hour = models.IntegerField(default=1)
    

    def __str__(self):
        return self.title


def upload_to_certi_photo_example(instance, file_name):
    return os.path.join(
        instance.owner.email,
        instance.challenge_name.title,
        "photo_ex",
        file_name,
    )
class OpenChallenge(models.Model):
    """ DURATIONS = (
        ("1주 동안", 1),
        ("2주 동안", 2),
        ("3주 동안", 3),
        ("4주 동안", 4),
    )
    challenge = models.ForeignKey("Challenge", on_delete=models.CASCADE, related_name="open_challenge", default="")
    start_day = models.DateField(null=True)
    duration = models.CharField(max_length=50, choices=DURATIONS, null=True)
    notice = models.TextField(blank=True)
    member = models.ManyToManyField(
        "user.Profile",
        through="ChallengeApply",
        related_name="challenge_apply",
    )
    number_of_applied_member = models.PositiveIntegerField(default=1) """
    pass

class ChallengeApply(models.Model):
    applied_id = models.AutoField(primary_key=True)
 
    created = models.DateTimeField(auto_now=True)
"""    challenge_id = models.ForeignKey(
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
    ) """


class Certification(models.Model):
    certification_id = models.AutoField(primary_key=True)
    challenge_id = models.ForeignKey(
        "Challenge",
        verbose_name="challenge name",
        on_delete=models.CASCADE,
        related_name="certification_challenge",
        default="",
    )
    user_profile_id = models.ForeignKey(
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
