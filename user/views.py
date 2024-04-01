from ast import literal_eval

import jwt.exceptions
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from access.utils.managers.frontend_managers import (
    AuthenticationRemoteManager,
)

from core.miniframework.exc import TokenExpiredError
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from user.utils.managers.managers import ProfileManager, MyChallengesManager



class UserCreateView(APIView):
    """
    (POST)      /api/user  회원 가입
    (PATCH)     /api/user  회원 정보 수정
    (DELETE)    /api/user   회원 정보 삭제
    """

    def post(self, request):
        req_data = request.data

        try:
            res = AuthenticationRemoteManager().request_sign_up(req_data)
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except serializers.ValidationError as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_201_CREATED)


class ProfileView(APIView):
    """
    """

    def get(self, request):
        try:
            res = ProfileManager().get_profile_info(
                access_token=request.headers["Access"]
            )
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except (serializers.ValidationError, IntegrityError) as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_200_OK)

class MyChallengeView(APIView):
    """
    (GET) /api/user/profile/my_challenges/  나의 챌린지 조회
    """
    def get(self, request):
        try:
            res = MyChallengesManager().get_my_challenges(
                access_token=request.headers["Access"]
            )
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except (serializers.ValidationError, IntegrityError) as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_200_OK)
    
   