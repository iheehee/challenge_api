from .models import Challenge, ChallengeApply
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

    def create(self, validated_data):
        user = self.context["user"]
        new_challenge = Challenge.objects.create(**validated_data, owner=user)
        ChallengeApply.object.create(challenge=new_challenge, user=user.profile)
        return new_challenge
