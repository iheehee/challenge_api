from abc import ABCMeta
from typing import Dict, Any
from collections.abc import Callable

from core.miniframework.manager_layer.manager_layer import BackendManagerLayer, FrontendManagerLayer
from core.miniframework.query_layer.access_query.authenticator import AuthenticateTokenGenerator
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS

class BaseManager(metaclass=ABCMeta):
    """
    모든 Manager의 최상위 객체
    전역으로 Manager에게 필요한 기능을 구현해야 할 경우 
    여기에 구현
    """

class AuthenticationManager(BaseManager,
                            BackendManagerLayer,
                            metaclass=ABCMeta):
    """
    인증 Manager

    데이터 검증 후, 검증이 완료되면 토큰을 전송한다.
    BackendManager 타입으로 View단위에서가 아닌 FrontendManager단에서 사용할 것

    :variable token_generator <AuthenticateTokenGenerator>: 토큰 생성기
    :variable check_auth <Function[Any] -> bool>: 토큰을 생성하기 전 유효한 사용자 인지 검수를 한다.
    """

    token_generator: AuthenticateTokenGenerator
    check_auth: Callable

    def auth(self, info_for_token: Any, *args, **kwargs) -> str:
        """
        토큰 발행

        :param info_for_token: 토큰을 만들기 위한 정보들
        :param args, kwargs: info_for_token을 제외한 나머지 parameter로 사용자 검토를 할 때 사용된다.

        :return: 문자열 형태의 토큰을 발행

        :exception PermissionError: 유효하지 않은 사용자일 경우
        """
        print(*args)
        if self.check_auth(*args, **kwargs):
            return self.token_generator.generate(info_for_token)
        else:
            raise PermissionError('Auth Failed')


class CRUDManager(BaseManager, FrontendManagerLayer, metaclass=ABCMeta):
    """
    데이터베이스를 조작하기 위한 Manager

    variable cruds_query: 기초 쿼리 함수 제공하는 클래스
    """
    cruds_query: QueryCRUDS

    def _create(self, *args, **kwargs):
        return self.cruds_query.create(*args, **kwargs)
    
    def _update(self, *args, **kwargs):
        return self.cruds_query.update(*args, **kwargs)

    def _read(self, *args, **kwargs):
        return self.cruds_query.read(*args, **kwargs)

    def _destroy(self, *args, **kwargs):
        return self.cruds_query.destroy(*args, **kwargs)

    def _search(self, *args, **kwargs):
        return self.cruds_query.search(*args, **kwargs)
