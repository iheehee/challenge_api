from challenge.utils.queries import ChallengeQuery
from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
)

from core.miniframework.manager_layer.manager import CRUDManager
from core.miniframework.system_layer.jwt.jwt import read_jwt


class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
        return self._read(pk)

    def update_challenge(self, challenge_data, access_token):
        # 토큰 데이터 추출
        issue, email = read_jwt(access_token)
        User = User.objects.get(email=email)

        is_available = LoginOnly(issue)
        if not bool(is_available):
            raise PermissionError("Permission Failed")

        return self._update(
            modified_challenge_data=challenge_data,
        )
