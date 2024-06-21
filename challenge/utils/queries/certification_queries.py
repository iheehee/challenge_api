from typing import Any, Dict, List, Optional

from django.db import transaction

from challenge.models import Certification, Challenge, ChallengeApply
from challenge.serializers import CertificationSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryCreator,
    QueryDestroyer,
    QueryReader,
    QueryUpdator,
)
from core.miniframework.tools.pagination import CustomPagination


class CertificationQueryReader(QueryReader, CustomPagination):
    """챌린지 인증을 조회하는 쿼리"""

    page_size = 5
    challenge = None

    def __call__(self, request, pk):
        
        certification_query = Certification.objects.filter(challenge_id=pk)
        """ pagination_query = self.paginated_query_set(
        request=request, query_set=challenge
            ) """
        serializer = CertificationSerializer(instance=certification_query, many=True)
        result={"challenge_id": pk,
                "certifications": serializer.data}
        return result
        #return self.paginated_response(request, pagination_query, serializer.data)

        """ else:
            challenge = Certification.objects.filter(certification_id=certification_id) """

        #return challenge


class CertificationQueryCreator(QueryCreator):
    """챌린지 인증을 위한 쿼리"""

    @transaction.atomic()
    def __call__(self, challenge_id, user_profile_id, certification_num, certification_local_photo_url, image):

        data = {
            "challenge_id": challenge_id,
            "user_profile_id": user_profile_id,
            "certification_num": certification_num,
            "certification_local_photo_url": certification_local_photo_url,
            "certification_photo": image,
        }
        """
        | 인증을 건너뛴 상태에서는 data 객체 내 certification_photo와 certification_local_photo_url 키의 데이터 값은 ""(빈문자열)이 된다.
        """
        serializer = CertificationSerializer(data=data)
        
        if serializer.is_valid():
            serializer.save()
        else:
            raise ValueError()

        return serializer.data

class CertificationeQueryUpdator(QueryUpdator):
    """챌린지 인증 내용을 업데이트하기 위한 쿼리"""
    def __call__(self, challenge_id, certification_num, image, data):

        target_certification = Certification.objects.get(
            challenge_id=challenge_id, certification_num=certification_num
            )
        serializer = CertificationSerializer(target_certification, data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        message = "인증 정보를 수정 하였습니다."
        return message

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
    updator = CertificationeQueryUpdator()
    destroyer = CertificationQueryDestroyer()
