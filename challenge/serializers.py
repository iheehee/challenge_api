from .models import Challenge, Certification, CertificationDetail
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

 
class CertificationDetailSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = CertificationDetail
        fields = (
            "certification_num",
            "certification_date",
            "certification_photo",
            "certification_local_photo_url",
            "certification_comment",
        )
    def create(self, validated_data):
        certification = self.context['certification']
        new_certification_detail = CertificationDetail.objects.create(**validated_data, certification_id=certification)

        return new_certification_detail

class CertificationSerializer(serializers.ModelSerializer):
    certifications = CertificationDetailSerializer(many=True, read_only=True)

    class Meta:
        model = Certification
        fields = (
            "id",
            "user_profile_id",
            "challenge_id",
            "certifications",
        )
        read_only_fields = ("id",)

