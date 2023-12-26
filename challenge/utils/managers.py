from challenge.utils.queries import ChallengeQuery
from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
)
from core.miniframework.query_layer.access_query.permission import (
    PermissionSameUserChecker as IsOwner,
)

from core.miniframework.manager_layer.manager import CRUDManager
from core.miniframework.system_layer.jwt.jwt import read_jwt

from user.models import User
from challenge.models import Challenge


class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
        return self._read(pk)

    def update_challenge(self, challenge_data, challenge_id, access_token):
        # 토큰 데이터 추출

        issue, user_email = read_jwt(access_token)
        user = User.objects.get(email=user_email)
        target_challenge = Challenge.objects.get(id=challenge_id)

        """
        로그인 한  상태이면서 내가 만든 챌린지 이거나 관리자일 경우 수정이 가능하다.
        """

        print(IsOwner(user_email, target_challenge.owner))
        is_available = LoginOnly(issue) & IsOwner(user_email, target_challenge.owner)

        if not bool(is_available):
            raise PermissionError("Permission Failed")

        return self._update(
            modified_challenge_data=challenge_data,
        )
