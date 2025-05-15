from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model # settings.AUTH_USER_MODEL 기반으로 User 모델 가져오기

# get_user_model()을 통해 프로젝트의 User 모델을 참조
User = get_user_model()

@database_sync_to_async
def get_user(token):
    try:
        validated_token = AccessToken(token)
        user_id = validated_token["user_id"]
        return User.objects.get(id=user_id)
    except Exception:
        return AnonymousUser()
    # JWT 토큰을 검증하고, user_id로 User 객체를 조회하여 반환. 검증에 실패하면 AnonymousUser 반환

class JWTAuthMiddleware:
    def __init__(self, inner):
        self.inner = inner

    def __call__(self, scope):
        return JWTAuthMiddlewareInstance(scope, self.inner)
    # AuthMiddlewareStack 대신 사용할 커스텀 JWT 인증 미들웨어. 쿼리스트링 ?token=... 으로 전달된 JWT를 파싱하여 scope['user']에 할당

class JWTAuthMiddlewareInstance:
    def __init__(self, scope, inner):
        self.scope = dict(scope)
        self.inner = inner
    async def __call__(self, receive, send):
        raw_qs = self.scope.get("query_string", b"").decode()
        params = parse_qs(raw_qs)
        token = params.get("token", [None])[0]

        if token:
            self.scope['user'] = await get_user(token)
        else:
            self.scope['user'] = AnonymousUser()

        inner = self.inner(self.scope)
        return await inner(receive, send)
