from challenge.utils.queries import ChallengeQuery
from core.miniframework.manager_layer.manager import CRUDManager

class ChallengeManager(CRUDManager):
    cruds_query = ChallengeQuery()

    def get_challenge_info(self, pk=None):
    
        return self._read(pk)