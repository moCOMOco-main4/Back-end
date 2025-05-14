from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.posts.models.post import Post
from apps.posts.models.application import Application
from apps.posts.models.post_like import PostLike
from apps.app_users.models import User


# 모집글 생성용
class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    backend = serializers.IntegerField(required=False, default=0)
    frontend = serializers.IntegerField(required=False, default=0)
    designer = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer'
        ]

    def create(self, validated_data):
        roles = {
            "backend": validated_data.pop("backend", 0),
            "frontend": validated_data.pop("frontend", 0),
            "designer": validated_data.pop("designer", 0),
        }
        post = Post.objects.create(**validated_data, roles=roles)
        return post


# 모집글 목록 조회용 (상우님 기준)
class PostListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'is_closed',
            'date', 'place_name', 'latitude', 'longitude', 'max_people'
        ]


# 모집글 상세 조회용 (상우님 기준)
class PostDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "nickname": obj.user.nickname,
            "email": obj.user.email,
            "profile_image": obj.user.profile_image.url if obj.user.profile_image else None
        }

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(user=user, post=obj).exists()

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()


# 모집글 수정용 (상우님 기준)
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed'
        ]


# 비율형 상세 조회용 (선형님 기준)
class PostSimpleDetailSerializer(serializers.ModelSerializer):
    current_people = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'max_people', 'current_people']

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()
