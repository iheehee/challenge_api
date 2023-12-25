from core.miniframework.query_layer.access_query.permission import (
    PermissionIssueChecker,
    PermissionLevelChecker,
)


class SignUpPermissionChecker(PermissionIssueChecker):
    issue = "sign-up"


class LoginPermissionChecker(PermissionIssueChecker):
    issue = "login"


class FindingPasswordPermissionChecker(PermissionIssueChecker):
    issue = "finding-password"


class AdminPermissionChecker(PermissionLevelChecker):
    level = "admin"
