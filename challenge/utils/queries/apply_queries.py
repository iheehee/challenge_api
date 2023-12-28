from challenge.models import Challenge, ChallengeApply, Certification
from challenge.serializers import ChallengeSerializer
from core.miniframework.query_layer.data_query.query_cruds import QueryCRUDS
from core.miniframework.query_layer.data_query.query_methods import (
    QueryReader,
    QueryCreator,
    QueryDestroyer,
    QueryUpdator,
)


class ChallengeApplyQuery(QueryCRUDS):
    pass
