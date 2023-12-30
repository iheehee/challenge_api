from ast import literal_eval

import django.db.utils
import jwt.exceptions
from rest_framework import status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView

from challenge.utils.managers import ChallengeManager, ChallengeApplyManager
from core.miniframework.exc import TokenExpiredError
from django.core.exceptions import ValidationError


# Create your views here.
class ChallengeView(APIView):
    """
    (GET) /api/challenge    챌린지 리스트뷰
    """

    def get(self, request):
        try:
            res = ChallengeManager().get_challenge_info()

        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(res, status.HTTP_200_OK)


class ChallengeCreateView(APIView):
    """
    (POST)  /api/company    회사 생성
    """

    def post(self, request):
        req_data = request.data
        try:
            res = ChallengeManager().create_challenge(
                challenge_data=req_data, access_token=request.headers["Access"]
            )
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except (serializers.ValidationError, django.db.utils.IntegrityError) as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_201_CREATED)


class ChallengeDetailView(APIView):
    """
    (GET) /api/challenge/<pk:int>       챌린지 상세보기
    (PUT) /api/challenge/<pk:int>       챌린지 정보 수정
    (DELETE) /api/challenge/<pk:int>    챌린지 삭제
    """

    def get(self, request, pk):
        try:
            res = ChallengeManager().get_challenge_info(pk)

        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(res, status.HTTP_200_OK)

    def put(self, request, pk):
        """
        permission 관리자, 클라이언트이면서 개설한 챌린지가 내 것인 상태
        """
        try:
            req_data = request.data
            res = ChallengeManager().update_challenge(
                req_data, challenge_id=pk, access_token=request.headers["Access"]
            )

        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except ValueError as e:
            return Response({"error": "수정하고자 하는 값이 없습니다."}, status.HTTP_404_NOT_FOUND)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except Exception as e:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_200_OK)

    def delete(self, request, pk):
        try:
            res = ChallengeManager().remove_challenge(
                challenge_id=pk,
                access_token=request.headers["Access"],
            )
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except ValueError:
            return Response({"error": "삭제하고자 하는 회사가 없습니다."}, status.HTTP_404_NOT_FOUND)
        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status=status.HTTP_204_NO_CONTENT)


class ChallengeApplyView(APIView):
    """
    (POST) /api/challenge/<pk:int>/apply    챌린지 가입하기
    (DELETE) /api/challenge/<pk:int>/apply  챌린지 탈퇴
    """

    def post(self, request, pk):
        try:
            res = ChallengeApplyManager().apply_challenge(
                challenge_id=pk, access_token=request.headers["Access"]
            )
        # except
        except KeyError:
            return Response({"error": "접근할 수 없는 API 입니다."}, status.HTTP_403_FORBIDDEN)
        except TokenExpiredError:
            return Response({"error": "토큰이 만료되었습니다."}, status.HTTP_403_FORBIDDEN)
        except (PermissionError, jwt.exceptions.DecodeError):
            return Response({"error": "유효한 토큰이 아닙니다."}, status.HTTP_403_FORBIDDEN)
        except (serializers.ValidationError, django.db.utils.IntegrityError) as e:
            return Response(str(e), status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"error": "챌린지 참여 인원이 다 찼습니다."})
        except Exception:
            return Response(
                {"error": "server error"}, status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        return Response(res, status.HTTP_201_CREATED)
