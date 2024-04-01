from typing import Optional

from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)
from user.models import Profile, User
from user.serializers import ProfileSerializer, UserSerializer


class MyChallengesQueryReader(QueryReader):
    """
    나의 챌린지 정보 읽기
    """
    def __call__(self, query_set: Optional[object]):
        
        try:
            result = []
            my_challenge_query_set = query_set.nickname_id.my_closed_challenges.all()
            for challenge in my_challenge_query_set:
                container = {}
                container['id'] = challenge.id
                container['title'] = challenge.title
                container['summery'] = challenge.summery
                container['max_hour'] = challenge.max_hour
                result.append(container)

            return result
            
        except:
            message = {"result": "개설된 챌린지가 업습니다."}
            return message


class MyChallengesQuery(QueryCRUDS):
    reader = MyChallengesQueryReader()
    