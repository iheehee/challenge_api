from core.miniframework.query_layer.access_query.permission import (
    PermissionIssueChecker,
    PermissionLevelChecker,
    PermissionSameUserChecker,
)


class SignUpPermissionChecker(PermissionIssueChecker):
    issue = "sign-up"


class LoginPermissionChecker(PermissionIssueChecker):
    issue = "login"


class FindingPasswordPermissionChecker(PermissionIssueChecker):
    issue = "finding-password"


class AdminPermissionChecker(PermissionLevelChecker):
    level = "admin"


class IsOwnerPermissionChechker(PermissionSameUserChecker):
    target_user = None
