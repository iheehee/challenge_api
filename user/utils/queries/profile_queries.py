from typing import Optional

from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)

from user.models import Profile
from user.serializers import ProfileSerializer, UserSerializer


class ProfilerQueryReader(QueryReader):
    """
    유저 프로파일 정보 읽기
    """

    def __call__(self, query_set: Optional[object]):
        """ 
        try:
            profile_query_result = query_set.profile

        except Profile.DoesNotExist:
            return None """
        return ProfileSerializer(query_set).data


class ProfileQuery(QueryCRUDS):
    reader = ProfilerQueryReader()
    
