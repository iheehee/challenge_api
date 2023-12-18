from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.utils.managers import ChallengeManager
# Create your views here.
class ChallengeView(APIView):
    """
    (GET) /api/challenge 챌린지 리스트뷰
    """
    def get(self, request):
        try:
            res = ChallengeManager() \
                .get_challenge_info()
            
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(res, status.HTTP_200_OK)

class ChallengeDetailView(APIView):
    """
    (GET) /api/challenge/<pk:int>       챌린지 상세보기
    (PUT) /api/challenge/<pk:int>       챌린지 정보 수정
    (DELETE) /api/challenge/<pk:int>    챌린지 삭제
    """
    def get(self, request, pk):
        try:
            res = ChallengeManager() \
                .get_challenge_info(pk)
            
        except Exception:
            return Response({'error': 'server error'},
                            status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(res, status.HTTP_200_OK)
    
    def put(self, request, pk):
        pass