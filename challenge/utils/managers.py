from access.utils.permissions import USER_LEVEL_MAP
from access.utils.permissions import AdminPermissionChecker as AdminOnly
from access.utils.permissions import ClientPermissionChecker as ClientOnly
from access.utils.permissions import LoginPermissionChecker as LoginOnly
from challenge.models import Challenge
from challenge.utils.queries.apply_queries import ChallengeApplyQuery
from challenge.utils.queries.certification_queries import CertificationQuery
from challenge.utils.queries.challenge_queries import ChallengeQuery
from core.miniframework.manager_layer.manager import CRUDManager
from core.miniframework.query_layer.access_query.permission import (
    PermissionAllAllowed as AllAllow,
)
from core.miniframework.query_layer.access_query.permission import (
    PermissionJoinedUserChecker as JoinedUser,
)
from core.miniframework.query_layer.access_query.permission import (
    PermissionSameUserChecker as IsOwner,
)
from core.miniframework.system_layer.jwt.jwt import read_jwt
from user.models import Profile, User


class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
        return self._read(pk)

    def create_challenge(self, challenge_data, access_token):
        """
        챌린지 생성

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        유저 생성 실패: serializers.ValidationError
        """
        # 토큰 데이터 추출
        issue, email = read_jwt(access_token)
        user = User.objects.select_related("nickname_id").get(email=email)
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
        target_challenge = Challenge.objects.select_related("owner").filter(
            id=challenge_id
        )

        if len(target_challenge) == 0:
            raise ValueError("Value Error")

        target_challenge_owner = target_challenge.first().owner.email

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
        return self._destroy(challenge=target_challenge)


class ChallengeApplyManager(CRUDManager):
    cruds_query = ChallengeApplyQuery()

    def apply_challenge(self, challenge_id, access_token):
        """
        챌린지 참여

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """

        # 토큰 데이터 추출
        issue, user_email = read_jwt(access_token)
        print(user_email)
        user = User.objects.get(email=user_email)
        user_lv = USER_LEVEL_MAP[user.level]

        target_challenge_owner = Challenge.objects.filter(
            id=challenge_id
        ).select_related("owner")[0]

        target_challenge_member_list = Challenge.objects.filter(
            id=challenge_id
        ).prefetch_related("profile_set")

        """ 
        챌린지에 참여하려면 로그인 상태여야 한다.
        클라이언트 레벨이어야 한다.
        본인이 만든 챌린지가 아니어야 한다.
        이미 참여한 참여자가 아니어야 한다.
        """

        is_available = LoginOnly(issue) & ClientOnly(user_lv)
        is_owner_joined = IsOwner(
            user_email, target_challenge_owner.owner.email
        ) & JoinedUser(user.profile, target_challenge_member_list)

        if not bool(is_available):
            raise PermissionError("Permission Failed")
        if bool(is_owner_joined):
            raise PermissionError("Permission Failed")
        # 생성
        return self._create(challenge_id=challenge_id, user=user)

    def remove_applied_challenge(self, challenge_id, access_token):
        """
        참여한 챌린지 탈퇴

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """
        issue, user_email = read_jwt(access_token)
        user = User.objects.get(email=user_email)
        user_lv = USER_LEVEL_MAP[user.level]
        challenge_member_list = Challenge.objects.get(id=challenge_id).member.all()

        """ 
        챌린지에 참여하려면 로그인 상태여야 한다.
        클라이언트 레벨이어야 한다.
        가입된 챌린지에 한에서 탈퇴할 수 있다.
        """
        is_available = (LoginOnly(issue) & ClientOnly(user_lv)) & JoinedUser(
            user.profile, challenge_member_list
        )

        if not bool(is_available):
            raise PermissionError("Permission Failed")

        # 삭제
        return self._destroy(challenge_id=challenge_id, user=user)


class CertificationManager(CRUDManager):
    cruds_query = CertificationQuery()

    def create_certification(self, access_token, data, image):
        """
        챌린지 인증

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """
        # 토큰 데이터 추출
        issue, user_email = read_jwt(access_token)
        user = User.objects.select_related("nickname_id").get(email=user_email)
        user_email = user.email
        user_lv = USER_LEVEL_MAP[user.level]

        # key_list = ['challenge_id', 'certification_num', 'certification_local_photo_url']
        challenge_id = data["challenge_id"]
        certification_num = data["certification_num"]
        
        # created_challenge_list = user.nickname_id.my_closed_challenges.all()
        # joined_member_list = target_challenge_member_list[0].member.all()
        target_challenge = Challenge.objects.select_related("owner").filter(
            id=challenge_id
        )

        if len(target_challenge) == 0:
            raise ValueError("Value Error")

        target_challenge_owner = target_challenge.first().owner.email
        """ 
        챌린지 인증을 하려면 로그인 상태여야 한다.
        클라이언트 레벨이어야 한다.
        내가 만든 챌린지어야 한다.
        진행 중인 챌린지어야 한다.(쿼리단에서 구현)
        """

        is_available = (
            IsOwner(user_email, target_challenge_owner) | AdminOnly(user_lv)
        ) & LoginOnly(issue)
        if not bool(is_available):
            raise PermissionError("Permission Failed")
        user_profile_id = user.nickname_id.id
        
        # 생성
        return self._create(
            challenge_id,
            user_profile_id,
            certification_num,
            image,
        )

    def modify_certification(self, access_token, data, image):
        """
        챌린지 인증 수정

        디코딩 실패: jwt.exceptions.DecodeError
        토큰 만료: TokenExpiredError
        권한이 안됨: PermissionError
        알수 없는 에러: exception
        """
        print(data)
        issue, user_email = read_jwt(access_token)
        user = User.objects.select_related("nickname_id").get(email=user_email)
        user_email = user.email
        user_lv = USER_LEVEL_MAP[user.level]
        
        challenge_id = data["challenge_id"]
        certification_num = data["certification_num"]
        

        target_challenge = Challenge.objects.select_related("owner").filter(
            id=challenge_id
        )

        if len(target_challenge) == 0:
            raise ValueError("Value Error")

        target_challenge_owner = target_challenge.first().owner.email
        """ 
        챌린지 인증을 하려면 로그인 상태여야 한다.
        클라이언트 또는 관리자 레벨이어야 한다.
        내가 만든 챌린지어야 한다.
        진행 중인 챌린지어야 한다.(쿼리단에서 구현)
        """
        is_available = (
            IsOwner(user_email, target_challenge_owner) | AdminOnly(user_lv)
        ) & LoginOnly(issue)
        if not bool(is_available):
            raise PermissionError("Permission Failed")

        
        return self._update(challenge_id, certification_num, image, data)

    def get_certification_info(self, request, pk):

        return self._read(request, pk)


def remove_certification(self, certification_id, access_token):
    """ """
    # 토큰 데이터 추출
    issue, user_email = read_jwt(access_token)
    user = User.objects.get(email=user_email)
    user_lv = USER_LEVEL_MAP[user.level]

    """
    인증을 삭제하려면 로그인 상태여야 한다.
    클라이언트 레벨 또는 관리자 레벨이어야 한다.
    """
    is_available = (AdminOnly(user_lv) | ClientOnly(user_lv)) & LoginOnly(issue)
    if not bool(is_available):
        raise PermissionError("Permission Failed")

    # 삭제
    return self._destroy(certification_id, access_token)
