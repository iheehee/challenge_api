from typing import Dict, Optional, List, Any

from django.db import transaction

from challenge.models import Challenge, ChallengeApply
from challenge.serializers import ChallengeSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
)
from django.core.exceptions import ValidationError


class ChallengeQueryApply(QueryCreator):
    """챌린지 참여를 위한 쿼리"""

    @transaction.atomic()
    def __call__(self, challenge_id, user):
        """
        챌린지의 최대 인원이 모두 차있다면 참여할 수 없다.
        """
        target_challenge = Challenge.objects.get(id=challenge_id)
        if target_challenge.number_of_applied_member > target_challenge.max_member:
            raise ValidationError("인원이 모두 찼습니다.")

        ChallengeApply.objects.create(challenge_id=challenge_id, user=user.profile)
        target_challenge.number_of_applied_member += 1
        target_challenge.save()
        message = "챌린지에 참가되었습니다."
        return message


class ChallengeQueryLeave(QueryDestroyer):
    """챌린지 탈퇴를 위한 쿼리"""

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


class ChallengeApplyQuery(QueryCRUDS):
    creator = ChallengeQueryApply()
    destroyer = ChallengeQueryLeave()
