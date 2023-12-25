from rest_framework import serializers

from core.miniframework.tools.password import hash_password
from user.models import User


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        # password 암호화

        validated_data["password"] = hash_password(validated_data["password"])
        # Save data
        user = User(**validated_data)
        user.save()

        return user

    class Meta:
        model = User
        fields = (
            "nickname",
            "email",
            "password",
        )
