from typing import Optional

from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)

from user.models import User
from user.serializers import UserSerializer


class UserQueryReader(QueryReader):
    """
    유저 정보 읽기
    """

    def __call__(self, email: Optional[str] = None, nickname: Optional[str] = None):
        obj = None
        try:
            if email:
                obj = User.objects.get(email=email)
            elif nickname:
                obj = User.objects.get(nickname=nickname)
        except User.DoesNotExist:
            return None
        return UserSerializer(obj).data


class UserQueryCreator(QueryCreator):
    """
    유저 생성
    """

    def __call__(self, data):
        user_serializer = UserSerializer(data=data)
        user_serializer.is_valid(raise_exception=True)
        user_serializer.save()
        data = user_serializer.data
        # password 부분 삭제
        del data["password"]
        return data


class UserQuery(QueryCRUDS):
    reader = UserQueryReader()
    creator = UserQueryCreator()
