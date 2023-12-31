from abc import ABCMeta, abstractmethod
from typing import Any, Optional


class PermissionChecker(metaclass=ABCMeta):
    """
    사용자 권한을 체크하는 데 사용된다.
    """

    checked: Optional[bool] = None
    data: Any = None

    def __init__(self, data: Any):
        self.data = data

    def __bool__(self):
        if self.checked is None:
            raise TypeError("This instance is not checked")
        return self.checked

    def __and__(self, other):
        if self.checked is None:
            self.check()
        if not self.checked:
            other.checked = False
        else:
            if other.checked is None:
                other.check()
            other.checked &= self.checked

        return other

    def __or__(self, other):
        if self.checked is None:
            self.check()
        if self.checked:
            other.checked = True
        else:
            if other.checked is None:
                other.check()
            other.checked |= self.checked
        return other

    @abstractmethod
    def check(self) -> bool:
        """
        사용자 권한 체크
        """
        pass


class PermissionSameUserChecker(PermissionChecker):
    """
    해당 유저가 같은 유저인 지 확인한다.

    예를 들어 회사를 삭제할 경우 해당 회사를 만든 사람만이 삭제할 수 있어야 한다.
    """

    target_user: Optional[str] = None

    def __init__(self, data, target_user=None):
        super().__init__(data)
        self.target_user = target_user

    def check(self) -> bool:
        # print(self.data == self.target_user)
        self.checked = self.data == self.target_user


class PermissionJoinedUserChecker(PermissionChecker):
    """
    해당 유저의 챌린지 가입 여부를 확인한다.

    챌린지에 가입한 유저는 또 가입할 수 없다.
    챌린지에 가입한 유저여야만 탈퇴를 할 수 있다.
    """

    target_challenge_member_list: Optional[list] = None

    def __init__(self, data, target_challenge_member_list=None):
        super().__init__(data)
        self.target_challenge_member_list = target_challenge_member_list

    def check(self) -> bool:
        # print(self.data in self.target_challenge_member_list)
        self.checked = self.data in self.target_challenge_member_list


class PermissionLevelChecker(PermissionChecker, metaclass=ABCMeta):
    """
    사용자의 수준(Admin, Client 등...)을 체크한다.
    """

    level: Any

    def __init__(self, data):
        super().__init__(data)

    def check(self) -> bool:
        self.checked = self.data == self.level


class PermissionIssueChecker(PermissionChecker, metaclass=ABCMeta):
    """
    사용자의 목표를 체크한다.

    예를 들어 패스워드 변경이나, 회원 가입이 이에 포함된다.
    """

    issue: Any

    def __init__(self, data):
        super().__init__(data)

    def check(self) -> bool:
        self.checked = self.data == self.issue


class PermissionAllAllowed(PermissionChecker):
    """
    모든 조건 허용
    """

    def __init__(self, data):
        super().__init__(data)

    def check(self) -> bool:
        self.checked = True
