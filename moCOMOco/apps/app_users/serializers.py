# apps/app_users/serializers.py
from rest_framework import serializers
from dj_rest_auth.serializers import JWTSerializer
from .models import User

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'nickname', 'name', 'phone',
            'github_url', 'portfolio_url', 'intro',
            'position', 'position_name', 'provider', 'profile_image'
        ]
        read_only_fields = ['id', 'email', 'provider']

class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'nickname']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'nickname', 'phone', 'github_url',
            'portfolio_url', 'intro', 'profile_image'
        ]

class PositionSerializer(serializers.Serializer):
    position = serializers.IntegerField()

class PositionResponseSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    position_id = serializers.IntegerField()
    position_name = serializers.CharField()

# JWT 응답 커스터마이징
class CustomJWTSerializer(JWTSerializer):
    user = UserDetailSerializer(read_only=True)
    isNewUser = serializers.BooleanField(default=False)

    class Meta:
        fields = ('access', 'refresh', 'user', 'isNewUser')

class UserProfileSerializer(serializers.ModelSerializer):
    """다른 사용자에게 공개되는 프로필 정보 시리얼라이저"""
    class Meta:
        model = User
        fields = [
            'id', 'nickname', 'name', 'github_url',
            'portfolio_url', 'intro', 'position',
            'position_name', 'profile_image'
        ]
