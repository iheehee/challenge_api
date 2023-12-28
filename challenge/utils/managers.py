from challenge.utils.queries.challenge_queries import ChallengeQuery
from challenge.utils.queries.apply_queries import ChallengeApplyQuery
from access.utils.permissions import (
    LoginPermissionChecker as LoginOnly,
    AdminPermissionChecker as AdminOnly,
    USER_LEVEL_MAP,
)
from core.miniframework.query_layer.access_query.permission import (
    PermissionSameUserChecker as IsOwner,
    PermissionAllAllowed as AllAllow,
)

from core.miniframework.manager_layer.manager import CRUDManager
from core.miniframework.system_layer.jwt.jwt import read_jwt

from user.models import User
from challenge.models import Challenge


class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
        return self._read(pk)

    def create_challenge(self, challenge_data, access_token):
        """
        회사 생성

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: serializers.ValidationError
        """

        # 토큰 데이터 추출
        issue, email = read_jwt(access_token)
        user = User.objects.get(email=email)
        user_lv = USER_LEVEL_MAP[user.level]
        # 챌린지를 만드려면 해당 유저는 로그인이 되어 있거나 Admin 이면 가능하다.
        if not bool(AdminOnly(user_lv) | LoginOnly(issue)):
            raise PermissionError("Permission Failed")

        # 생성
        return self._create(challenge_data=challenge_data, user=user)

    def update_challenge(self, challenge_data, challenge_id, access_token):
        # 토큰 데이터 추출
        issue, user_email = read_jwt(access_token)
        target_challenge_owner = Challenge.objects.get(id=challenge_id).owner.email

        """
        로그인 한  상태이면서 내가 만든 챌린지 이거나 관리자일 경우 수정이 가능하다.
        """

        is_available = LoginOnly(issue) & IsOwner(user_email, target_challenge_owner)

        if not bool(is_available):
            raise PermissionError("Permission Failed")

        return self._update(
            modified_challenge_data=challenge_data, challenge_id=challenge_id
        )

    def remove_challenge(self, challenge_id, access_token):
        """
        채린지 삭제

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        없는 챌린지를 삭제하려고 함: ValueError
        알수 없는 에러: exception
        """

        # 토큰 데이터 추출
        issue, user_email = read_jwt(access_token)
        user = User.objects.get(email=user_email)
        user_lv = USER_LEVEL_MAP[user.level]
        target_challenge_owner = Challenge.objects.get(id=challenge_id).owner.email

        """
        챌린지를 삭제하려면 
        본인이 만든 챌린지이거나 관리자일 경우만 삭제 가능하다.
        로그인 상태여야 한다.
        
        """
        is_available = (
            IsOwner(user_email, target_challenge_owner) | AdminOnly(user_lv)
        ) & LoginOnly(issue)

        if not bool(is_available):
            raise PermissionError("Permission Failed")

        self._destroy(challenge_id=challenge_id)


class ChallengeApplyManager(CRUDManager):
    cruds_query = ChallengeApplyQuery()

    def apply_challenge(self, challenge_id, access_token):
        """
        챌린지 참여

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유효하지 않은 값 입력: serializers.ValidationError
        """

        # 토큰 데이터 추출
        issue, user_email = read_jwt(access_token)
        user = User.objects.get(email=user_email)
        target_challenge_owner = Challenge.objects.get(id=challenge_id).owner.email
        """ 
        챌린지에 참여하려면 로그인 상태여야 한다.
        
        본인이 만든 챌린지에는 참여할 수 없다(쿼리단에서 구현).
        """
        is_available = LoginOnly(issue) & AllAllow()
        print(bool(is_available))
        if not bool(is_available):
            raise PermissionError("Permission Failed")

        # 생성
        return self._create(challenge_id=challenge_id, user=user)
