from typing import Optional

from access.utils.managers.backend_managers import LoginManager

from core.miniframework.manager_layer.manager import BaseManager
from core.miniframework.manager_layer.manager_layer import FrontendManagerLayer

class AuthenticationRemoteManager(BaseManager,
                                  FrontendManagerLayer):
    def request_login(self, email, password):
        token = LoginManager().auth(email, email, password)
        
        return token
