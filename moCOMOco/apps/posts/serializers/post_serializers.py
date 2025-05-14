from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.posts.models.post import Post
from apps.posts.models.application import Application
from apps.posts.models.post_like import PostLike
from apps.app_users.models import User


# 모집글 등록용
class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category', 'date', 'place_name', 'address',
            'latitude', 'longitude', 'max_people', 'roles', 'image'
        ]

    def validate_roles(self, value):
        if not isinstance(value, dict):
            raise serializers.ValidationError("roles 필드는 JSON 형식이어야 합니다.")
        for role, count in value.items():
            if not isinstance(role, str) or not isinstance(count, int):
                raise serializers.ValidationError("roles는 {역할: 인원수} 형식이어야 합니다.")
        return value


# 모집글 리스트 (상우님 요청 기준)
class PostListSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    is_writer = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'is_closed', 'date',
            'place_name', 'address', 'max_people',
            'status', 'role_status',
            'is_writer', 'is_applied', 'is_liked', 'img_url',
            'created_at', 'updated_at'
        ]

    @extend_schema_field(serializers.CharField())
    def get_status(self, obj):
        return Application.objects.filter(post=obj).count()

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_role_status(self, obj):
        result = {}
        for role in obj.roles.keys():
            count = Application.objects.filter(post=obj, role=role).count()
            result[role] = str(count)
        return result

    @extend_schema_field(serializers.BooleanField())
    def get_is_writer(self, obj):
        user = self.context['request'].user
        return user.is_authenticated and obj.user == user

    @extend_schema_field(serializers.BooleanField())
    def get_is_applied(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Application.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.BooleanField())
    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.URLField())
    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return request.build_absolute_uri('/media/posts/images/default.png')


# 작성자 정보
class WriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'nickname', 'profile_image']


# 참여자 정보
class ParticipantSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    nickname = serializers.CharField(source='user.nickname')
    profile_image = serializers.ImageField(source='user.profile_image')

    class Meta:
        model = Application
        fields = ['id', 'nickname', 'profile_image']


# 상우님 요청 모집글 상세 조회용
class PostDetailSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(source='user', read_only=True)
    participants = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category', 'date',
            'place_name', 'address', 'latitude', 'longitude',
            'is_closed', 'max_people', 'created_at', 'updated_at',
            'writer', 'participants', 'is_liked', 'is_applied',
            'img_url', 'current_people', 'role_status'
        ]

    @extend_schema_field(serializers.ListSerializer(child=ParticipantSerializer()))
    def get_participants(self, obj):
        applications = Application.objects.filter(post=obj)
        return ParticipantSerializer(applications, many=True).data

    @extend_schema_field(serializers.BooleanField())
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.BooleanField())
    def get_is_applied(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Application.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.URLField())
    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return request.build_absolute_uri('/media/posts/images/default.png')

    @extend_schema_field(serializers.IntegerField())
    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_role_status(self, obj):
        result = {}
        for role in obj.roles.keys():
            count = Application.objects.filter(post=obj, role=role).count()
            result[role] = str(count)
        return result


# 모집글 상세 조회용 (선형님 요청 기준)
class PostSimpleDetailSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(source='user', read_only=True)
    participants = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()
    role_status = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category', 'date',
            'place_name', 'address', 'latitude', 'longitude',
            'is_closed', 'max_people', 'created_at', 'updated_at',
            'writer', 'participants', 'is_liked', 'is_applied',
            'img_url', 'current_people', 'role_status'
        ]

    @extend_schema_field(serializers.ListSerializer(child=ParticipantSerializer()))
    def get_participants(self, obj):
        applications = Application.objects.filter(post=obj)
        return ParticipantSerializer(applications, many=True).data

    @extend_schema_field(serializers.BooleanField())
    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.BooleanField())
    def get_is_applied(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Application.objects.filter(post=obj, user=user).exists()
        return False

    @extend_schema_field(serializers.URLField())
    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return request.build_absolute_uri('/media/posts/images/default.png')

    @extend_schema_field(serializers.IntegerField())
    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()

    @extend_schema_field(serializers.DictField(child=serializers.CharField()))
    def get_role_status(self, obj):
        result = {}
        for role, max_count in obj.roles.items():
            current_count = Application.objects.filter(post=obj, role=role).count()
            result[role] = f"{current_count}/{max_count}"
        return result


# 모집글 수정
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'date', 'place_name', 'address',
            'latitude', 'longitude', 'max_people',
        ]


