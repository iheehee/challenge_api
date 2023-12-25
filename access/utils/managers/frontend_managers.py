from typing import Optional

from access.utils.managers.backend_managers import LoginManager

from core.miniframework.manager_layer.manager import BaseManager
from core.miniframework.manager_layer.manager_layer import FrontendManagerLayer
from user.utils.queries import UserQuery


class AuthenticationRemoteManager(BaseManager, FrontendManagerLayer):
    def request_login(self, email, password):
        token = LoginManager().auth(email, email, password)

        return token

    def request_sign_up(self, nickname, email, password):
        """
        회원 가입

        알수 없는 에러: exception
        유저 생성 실패: sereializers.ValidationError
        """

        # 유저 생성 및 보내기
        return UserQuery().create(
            nickname=nickname,
            email=email,
            password=password,
        )
