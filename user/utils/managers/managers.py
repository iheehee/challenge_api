from core.miniframework.manager_layer.manager import CRUDManager
from core.miniframework.system_layer.jwt.jwt import read_jwt

from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
    ClientPermissionChecker as ClientOnly,
    USER_LEVEL_MAP,
)

from user.utils.queries.profile_queries import ProfileQuery
from user.utils.queries.my_challenges_queries import MyChallengesQuery
from user.models import User


class ProfileManager(CRUDManager):

    cruds_query = ProfileQuery()

    def get_profile_info(self, access_token):
        """
        유저 프로필 조회

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """

        issue, email = read_jwt(access_token)
        user = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]
        # 프로필을 조회하려면 로그인이 되어 있거나 Admin 이 가능하다.
        is_available = AdminOnly(user_lv) | LoginOnly(issue)

        if not bool(is_available):
            raise PermissionError("Permission Failed")
        
        return self._read(query_set=user)


class MyChallengesManager(CRUDManager):

    cruds_query = MyChallengesQuery()

    def get_my_challenges(self, access_token):
        """
        나의 챌린지 조회

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """

        issue, email = read_jwt(access_token)
        
        user = User.objects.select_related('nickname_id').get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]
        # 프로필을 조회하려면 로그인이 되어 있거나 Admin 이 가능하다.
        is_available = AdminOnly(user_lv) | LoginOnly(issue)

        if not bool(is_available):
            raise PermissionError("Permission Failed")
        
        return self._read(query_set=user)
    
    