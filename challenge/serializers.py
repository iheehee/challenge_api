from .models import Challenge,  Certification
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
        new_challenge = Challenge.objects.create(**validated_data, owner=user)
        user.nickname_id.my_closed_challenges.add(new_challenge)

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
        #read_only_fields = ("certification_id",)
