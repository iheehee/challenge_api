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

    def __call__(self, request, pk):
        
        certification_query = Certification.objects.filter(challenge_id=pk)
        """ pagination_query = self.paginated_query_set(
        request=request, query_set=challenge
            ) """
        serializer = CertificationSerializer(instance=certification_query, many=True)
        
        return serializer.data
        #return self.paginated_response(request, pagination_query, serializer.data)

        """ else:
            challenge = Certification.objects.filter(certification_id=certification_id) """

        #return challenge


class CertificationQueryCreator(QueryCreator):
    """챌린지 인증을 위한 쿼리"""

    @transaction.atomic()
    def __call__(self, challenge_id, user_profile_id, certification_num, certification_local_photo_url, image):
        
        certification = Certification.objects.get(challenge_id=challenge_id)

        data = {
            "certification_num": certification_num,
            "certification_local_photo_url": certification_local_photo_url,
            "certification_photo": image,
        }
        """
        | 인증을 건너뛴 상태에서는 data 객체 내 certification_photo와 certification_local_photo_url 키의 데이터 값은 ""(빈문자열)이 된다.
        """
        serializer = CertificationSerializer(data=data, context={"certification":certification})
        serializer.is_valid()
        print(serializer.errors)
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
