from urllib.parse import parse_qs
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth import get_user_model # settings.AUTH_USER_MODEL 기반으로 User 모델 가져오기
from channels.sessions import CookieMiddleware

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


class JWTAuthMiddlewareInstance:
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        raw_qs = scope.get("query_string", b"").decode()
        params = parse_qs(raw_qs)
        token = params.get("token", [None])[0]

        if token:
            scope['user'] = await get_user(token)
        else:
            scope['user'] = AnonymousUser()

        return await self.inner(scope, receive, send)


def JWTAuthMiddlewareStack(inner):
    return CookieMiddleware(JWTAuthMiddlewareInstance(inner))