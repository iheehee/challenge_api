from .models import Challenge, Certification
from user.models import Profile
from rest_framework import serializers

""" class OpenChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = OpenChallenge
        fields = (
            "challenge",
            "start_day",
            "duration",
            "notice",
            "member",
            "certifications",
            "max_member",
            "number_of_applied_member",
        )
        """

class ChallengeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Challenge
        fields = (
            "id",
            "title",
            "owner",
            "title_banner",
            "summery",
            "max_hour",
        )
        read_only_fields = ("id",)

    def create(self, validated_data):
        user = self.context["user"]
        user_profile = user.nickname_id
        new_challenge = Challenge.objects.create(**validated_data, owner=user)
        user_profile.my_closed_challenges.add(new_challenge)
        #인증 기본테이블 생성
        Certification.objects.create(user_profile_id=user_profile, challenge_id=new_challenge)
        return new_challenge


class CertificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Certification
        fields = (
            "user_profile_id",
            "challenge_id",
            "certification_num",
            "certification_date",
            "certification_photo",
            "certification_local_photo_url",
            "certification_dairy",
        )
        read_only_fields = ()

