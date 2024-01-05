from typing import Dict, Optional, List, Any

from django.db import transaction

from challenge.models import Challenge, ChallengeApply, Certification
from challenge.serializers import CertificationSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)

from rest_framework.pagination import PageNumberPagination
from core.miniframework.tools.pagination import PaginationHandlerMixin


class CustomPagination(PageNumberPagination):
    page_size = 2


class CertificationQueryReader(QueryReader):
    """챌린지 인증을 조회하는 쿼리"""

    challenge = None

    def __call__(self, request, pk, certification_id):
        if certification_id == None:
            challenge = Certification.objects.filter(challenge_id=pk)

        else:
            challenge = Certification.objects.filter(certification_id=certification_id)

        return challenge


class CertificationQueryCreator(QueryCreator):
    """챌린지 인증을 위한 쿼리"""

    @transaction.atomic()
    def __call__(self, challenge_id, user, comment, image):
        """
        챌린지의 최대 인원이 모두 차있다면 참여할 수 없다.
        """

        data = {
            "challenge": challenge_id,
            "user": user.profile.id,
            "certification_photo": image,
            "certification_comment": comment,
        }

        serializer = CertificationSerializer(data=data)
        serializer.is_valid()
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError()

        return serializer.data


class CertificationRemoveQuery(QueryDestroyer):
    """인증 삭제를 위한 쿼리"""

    def __call__(self, challenge_id, user):
        try:
            target_Applied_challenge = ChallengeApply.objects.get(
                user=user.profile, challenge_id=challenge_id
            )
        except:
            raise ValueError("삭제하고자 하는 챌린지가 없습니다.")
        target_Applied_challenge.delete()
        message = "챌린지를 탈퇴하였습니다."
        return message


class CertificationQuery(QueryCRUDS):
    reader = CertificationQueryReader()
    creator = CertificationQueryCreator()
    # destroyer = ChallengeQueryLeave()
