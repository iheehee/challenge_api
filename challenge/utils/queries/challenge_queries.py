from typing import Dict, Optional, List, Any

from django.db import transaction
from django.db.models import Q

from challenge.models import Challenge
from challenge.serializers import ChallengeSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)


# noinspection PyUnresolvedReferences
class ChallengeQueryReader(QueryReader):
    # 챌린지 불러오기
    challenge = None

    def __call__(self, pk):
        if pk == None:
            challenge = Challenge.objects.all()

        else:
            challenge = Challenge.objects.filter(id=pk)
        serializer = ChallengeSerializer(challenge, many=True)

        return serializer.data


class ChallengeQueryCreator(QueryCreator):
    @transaction.atomic()
    def __call__(self, challenge_data, user):
        serializer = ChallengeSerializer(data=challenge_data, context={"user": user})
        serializer.is_valid()
        serializer.save()
        message = {"result": "챌린지가 개설되었습니다"}
        return message


class ChallengeQueryUpdator(QueryUpdator):
    @transaction.atomic()
    def __call__(self, modified_challenge_data, challenge_id):
        challenge = Challenge.objects.filter(id=challenge_id)[0]
        serializer = ChallengeSerializer(challenge, data=modified_challenge_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return serializer.data


class ChallengeQueryDestroyer(QueryDestroyer):
    @transaction.atomic()
    def __call__(self, challenge):
        challenge.delete()
        message = {"result": "챌린지가 개설되었습니다"}
        return message


class ChallengeQuery(QueryCRUDS):
    reader = ChallengeQueryReader()
    creator = ChallengeQueryCreator()
    updator = ChallengeQueryUpdator()
    destroyer = ChallengeQueryDestroyer()
