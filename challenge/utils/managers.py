from challenge.utils.queries import ChallengeQuery
from core.miniframework.manager_layer.manager import CRUDManager

class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
    
        return self._read(pk)
    
    def update_challenge(self, challenge_data, access_token):

        # 토큰 데이터 추출
        #issue, email = read_jwt(access_token, 'wanted-company-searcher')
        #User = User.objects.get(email=email)
        #user_lv = USER_LEVEL_MAP[user.level]

        #is_available = (CompanyOnly(user_lv) | AdminOnly(user_lv)) & LoginOnly(issue)
        #if not bool(is_available):
        #    raise PermissionError('Permission Failed')

        return self._update(
            modified_challenge_data=challenge_data,
        )