from .models import Challenge, ChallengeApply, Certification
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
            "duration",
            "start_time",
            "end_time",
            "notice",
            "member",
            "certifications",
            "max_member",
            "number_of_applied_member",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["user"]
        new_challenge = Challenge.objects.create(**validated_data, owner=user)
        ChallengeApply.object.create(challenge=new_challenge, user=user.profile)
        return new_challenge


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = (
            "certification_id",
            "challenge",
            "user",
            "certification_date",
            "certification_photo",
            "certification_comment",
        )
        read_only_fields = ("certification_id",)
