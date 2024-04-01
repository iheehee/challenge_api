from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from access.utils.managers.frontend_managers import AuthenticationRemoteManager


class LoginView(APIView):
    """
    (POST)   /api/auth/login     로그인
    """

    def post(self, request):
        """
        post-param
        {
            "email": <str:email>,
            "password": <str:password>
        }
        """
        # 데이터 추출
        req_data = request.data

        # 토큰 리턴
        try:
            token = AuthenticationRemoteManager().request_login(**req_data)
        except PermissionError:
            # 로그인 실패
            return Response({"error": "로그인 실패"}, status=status.HTTP_403_FORBIDDEN)
        except ValueError:
            # 잘못된 데이터
            return Response({"error": "잘못된 접근"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response({"token": token}, status=status.HTTP_200_OK)
