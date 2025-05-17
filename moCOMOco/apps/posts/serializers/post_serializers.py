from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.posts.models.post import Post
from apps.posts.models.application import Application
from apps.posts.models.post_like import PostLike
from apps.app_users.models import User


# 모집글 생성용 (post)
class PostCreateListSerializer(serializers.ModelSerializer):
    # 역할군 인원 수 (프론트에서 개별 입력)
    backend = serializers.IntegerField(required=False, write_only=True, default=0)
    frontend = serializers.IntegerField(required=False, write_only=True, default=0)
    designer = serializers.IntegerField(required=False, write_only=True, default=0)
    fullstack = serializers.IntegerField(required=False, write_only=True, default=0)
    image = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer', 'fullstack'
        ]

    def create(self, validated_data):
        roles = {
            "backend": validated_data.pop("backend", 0),
            "frontend": validated_data.pop("frontend", 0),
            "designer": validated_data.pop("designer", 0),
            "fullstack": validated_data.pop("fullstack", 0),
        }
        # 역할군 의 합을 max_people로 설정
        validated_data['max_people'] = sum(roles.values())

        post = Post.objects.create(**validated_data, roles=roles, user=self.context['user'])
        return post

# 모집글 목록 조회용 (get)
class PostListSerializer(serializers.ModelSerializer):
    people_status = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category',
            'place_name', 'address', 'date',
            'image', 'is_closed', 'max_people',
            'people_status', 'role_status',
            'is_writer', 'is_applied', 'is_liked',
        ]

    def get_people_status(self, obj):
        return Application.objects.filter(user=obj.user).count()

    def get_role_status(self, obj):
        return obj.roles

    def get_is_writer(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request and request.user.is_authenticated else False

    def get_is_applied(self, obj):
        request = self.context.get('request')
        return Application.objects.filter(post=obj, user=request.user).exists() if request and request.user.is_authenticated else False

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return PostLike.objects.filter(post=obj, user=request.user).exists() if request and request.user.is_authenticated else False

# 모집글 상세 조회용 (전체 정보 포함)
class PostDetailSerializer(serializers.ModelSerializer):
    writer = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()
    people_status = serializers.SerializerMethodField()
    participants = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'created_at', 'updated_at',
            'writer', 'is_liked', 'is_applied',
            'current_people', 'people_status',
            'participants', 'role_status',
            'is_writer'
        ]

    def get_writer(self, obj):
        # 작성자 정보: id, 닉네임, 프로필 이미지
        return {
            "id": obj.user.id,
            "nickname": obj.user.nickname,
            "profile_image": obj.user.profile_image.url if obj.user.profile_image else None
        }

    def get_is_liked(self, obj):
        user = self.context['request'].user
        return PostLike.objects.filter(user=user, post=obj).exists()

    def get_is_applied(self, obj):
        user = self.context['request'].user
        return Application.objects.filter(user=user, post=obj).exists()

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()

    def get_people_status(self, obj):
        return Application.objects.filter(post=obj).count()

    def get_participants(self, obj):
        # 참여자 요약 정보 리스트 (id, 닉네임, 프로필)
        return [
            {
                "id": app.user.id,
                "nickname": app.user.nickname,
                "profile_image": app.user.profile_image.url if app.user.profile_image else None
            }
            for app in Application.objects.filter(post=obj).select_related('user')
        ]

    def get_role_status(self, obj):
        # JSONField 형태로 저장된 역할별 인원수 반환
        return obj.roles

    def get_is_writer(self, obj):
        request = self.context.get('request')
        return request.user == obj.user if request and request.user.is_authenticated else False

# 모집글 수정용
class PostUpdateSerializer(serializers.ModelSerializer):
    # 수정 시에도 역할별 인원 받기
    backend = serializers.IntegerField(required=False, default=0)
    frontend = serializers.IntegerField(required=False, default=0)
    designer = serializers.IntegerField(required=False, default=0)
    fullstack = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer', 'fullstack'
        ]

    def update(self, instance, validated_data):
        roles = {
            "backend": validated_data.pop("backend", 0),
            "frontend": validated_data.pop("frontend", 0),
            "designer": validated_data.pop("designer", 0),
            "fullstack": validated_data.pop("fullstack", 0),
        }
        # 역할군의 합을 max_people로 설정
        validated_data['max_people'] = sum(roles.values())

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.roles = roles
        instance.save()
        return instance



# 참여비율 기반 간단 상세 조회
class PostSimpleDetailSerializer(serializers.ModelSerializer):
    current_people = serializers.SerializerMethodField()  # 현재 신청자 수
    status = serializers.SerializerMethodField()          # UI용 상태: 모집중 / 모집완료

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category',
            'place_name', 'image',
            'max_people', 'current_people',
            'is_closed', 'status',
        ]

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()

    def get_status(self, obj):
        current = self.get_current_people(obj)
        return "모집완료" if current >= obj.max_people else "모집중"

class PostListSerializerWithParticipants(PostListSerializer):
    participants = serializers.SerializerMethodField()
    people_status = serializers.SerializerMethodField()

    class Meta(PostListSerializer.Meta):
        fields = PostListSerializer.Meta.fields + ['participants', 'people_status']

    def get_participants(self, obj):
        applications = Application.objects.filter(post=obj).select_related('user')
        return [
            {
                "id": app.user.id,
                "nickname": app.user.nickname,
                "profile_image": app.user.profile_image.url if app.user.profile_image else None
            }
            for app in applications
        ]

    def get_people_status(self, obj):
        return Application.objects.filter(post=obj).count()