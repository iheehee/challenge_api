from access.utils.authenticates.login import LoginTokenGenerator, check_login

from core.miniframework.manager_layer.manager import AuthenticationManager


class LoginManager(AuthenticationManager):
    check_auth = check_login
    token_generator = LoginTokenGenerator() 