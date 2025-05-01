from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status


class SocialLoginURLView(APIView):
    """
    소셜 로그인 URL을 생성하는 뷰
    프론트엔드에서 사용자가 소셜 로그인 버튼을 클릭하면
    이 URL로 리다이렉트하여 소셜 로그인을 시작
    """
    permission_classes = [AllowAny]

    def get(self, request, provider):
        """소셜 로그인 URL 생성"""
        try:
            # 프론트엔드 URL 가져오기
            frontend_url = getattr(settings, 'FRONTEND_URL', 'http://localhost:3000')

            # 제공자별 로그인 URL 생성
            if provider == 'kakao':
                client_id = settings.KAKAO_CLIENT_ID
                redirect_uri = settings.KAKAO_REDIRECT_URI

                if not client_id:
                    return Response({"detail": "KAKAO_CLIENT_ID 환경 변수가 설정되지 않았습니다."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                frontend_callback =f"{settings.FRONTEND_URL}/auth/callback"

                login_url = (
                    f"https://kauth.kakao.com/oauth/authorize"
                    f"?client_id={client_id}"
                    f"&redirect_uri={redirect_uri}"
                    f"&response_type=code"
                    f"&scope=profile_nickname,account_email"
                    f"&state={frontend_callback}"
                )

            elif provider == 'naver':
                client_id = settings.NAVER_CLIENT_ID
                redirect_uri = settings.NAVER_REDIRECT_URI
                state = settings.NAVER_STATE

                if not client_id:
                    return Response({"detail": "NAVER_CLIENT_ID 환경 변수가 설정되지 않았습니다."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                login_url = (
                    f"https://nid.naver.com/oauth2.0/authorize"
                    f"?client_id={client_id}"
                    f"&redirect_uri={redirect_uri}"
                    f"&response_type=code"
                    f"&state={state}"
                )

            elif provider == 'github':
                client_id = settings.GITHUB_CLIENT_ID
                redirect_uri = settings.GITHUB_REDIRECT_URI

                if not client_id:
                    return Response({"detail": "GITHUB_CLIENT_ID 환경 변수가 설정되지 않았습니다."},
                                    status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                login_url = (
                    f"https://github.com/login/oauth/authorize"
                    f"?client_id={client_id}"
                    f"&redirect_uri={redirect_uri}"
                    f"&scope=user:email read:user"
                )

            else:
                return Response({"detail": "지원하지 않는 provider 입니다."},
                                status=status.HTTP_400_BAD_REQUEST)

            return Response({"login_url": login_url})

        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)