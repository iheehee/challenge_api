from abc import ABCMeta
from typing import Dict, Any
from collections.abc import Callable

from core.miniframework.manager_layer.manager_layer import BackendManagerLayer, FrontendManagerLayer

class BaseManager(metaclass=ABCMeta):
    """
    모든 Manager의 최상위 객체
    전역으로 Manager에게 필요한 기능을 구현해야 할 경우 
    여기에 구현
    """

class CRUDmanager(BaseManager, FrontendManagerLayer, metaclass=ABCMeta):
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
