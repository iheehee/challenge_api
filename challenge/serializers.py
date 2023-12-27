from .models import (
    Challenge,
)
from rest_framework import serializers


class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = (
            "id",
            "title",
            "owner",
            "title_banner",
            "summery",
            "description",
            "start_day",
            "frequency",
            "duration",
            "notice",
            "max_member",
            "number_of_applied_member",
            "start_time",
            "end_time",
            "notice",
            "member",
            "certifications",
        )
        read_only_fields = ("id",)
