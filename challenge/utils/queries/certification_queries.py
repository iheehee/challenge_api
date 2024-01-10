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

from core.miniframework.tools.pagination import CustomPagination


class CertificationQueryReader(QueryReader, CustomPagination):
    """챌린지 인증을 조회하는 쿼리"""

    page_size = 5
    challenge = None

    def __call__(self, request, pk, certification_id):
        if certification_id == None:
            challenge = Certification.objects.filter(challenge_id=pk)
            pagination_query = self.paginated_query_set(
                request=request, query_set=challenge
            )
            serializer = CertificationSerializer(pagination_query, many=True)
            return self.paginated_response(request, pagination_query, serializer.data)

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


class CertificationQueryDestroyer(QueryDestroyer):
    """인증 삭제를 위한 쿼리"""

    @transaction.atomic()
    def __call__(self, certification_id):
        try:
            target_certification = Certification.objects.get(
                certification_id=certification_id
            )
        except:
            raise ValueError("삭제하고자 하는 인증이 없습니다.")
        target_certification.delete()
        message = "챌린지을 삭제하였습니다."
        return message


class CertificationQuery(QueryCRUDS):
    reader = CertificationQueryReader()
    creator = CertificationQueryCreator()
    destroyer = CertificationQueryDestroyer()
