from typing import Dict, Optional, List, Any

from django.db import transaction
from django.db.models import Q

from challenge.models import Challenge, ChallengeApply, Certification
from challenge.serializers import ChallengeSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QuerySearcher,
    QueryDestroyer, QueryUpdator
)

from user.models import User


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

class ChallengeQueryUpdator(QueryUpdator):
    @transaction.atomic()
    def __call__(self, challenge_data, pk):

        

class ChallengeQuery(QueryCRUDS):
    reader = ChallengeQueryReader()
    updator = ChallengeQueryUpdator()
