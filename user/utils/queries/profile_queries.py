from typing import Optional

from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)

from user.models import Profile
from user.serializers import ProfileSerializer


class ProfilerQueryReader(QueryReader):
    """
    유저 프로파일 정보 읽기
    """

    def __call__(self, query_set: Optional[object]):
        profile_query_result = None
        try:
            profile_query_result = query_set.profile

        except Profile.DoesNotExist:
            return None
        return ProfileSerializer(profile_query_result).data


class UserQueryCreator(QueryCreator):
    """
    유저 생성
    """

    def __call__(self):
        # req = {"nickname": nickname, "password": password, "email": email}

        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        data = user_serializer.data
        # password 부분 삭제
        del data["password"]
        return data


class ProfileQuery(QueryCRUDS):
    reader = ProfilerQueryReader()
    creator = UserQueryCreator()
