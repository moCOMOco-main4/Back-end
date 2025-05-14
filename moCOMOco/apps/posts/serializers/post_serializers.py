from rest_framework import serializers
from drf_spectacular.utils import extend_schema_field

from apps.posts.models.post import Post
from apps.posts.models.application import Application
from apps.posts.models.post_like import PostLike
from apps.app_users.models import User


# 모집글 생성용
class PostCreateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)

    backend = serializers.IntegerField(
        required=False,
        default=0,
        help_text="백엔드 모집 인원 수",
    )
    frontend = serializers.IntegerField(
        required=False,
        default=0,
        help_text="프론트엔드 모집 인원 수",
    )
    designer = serializers.IntegerField(
        required=False,
        default=0,
        help_text="디자이너 모집 인원 수",
    )

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
        validated_data['roles'] = roles
        return Post.objects.create(**validated_data)


# 모집글 수정용
class PostUpdateSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(required=False)
    backend = serializers.IntegerField(required=False, default=0)
    frontend = serializers.IntegerField(required=False, default=0)
    designer = serializers.IntegerField(required=False, default=0)

    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'image', 'date', 'max_people', 'is_closed',
            'backend', 'frontend', 'designer'
        ]

    def update(self, instance, validated_data):
        roles = {
            "backend": validated_data.pop("backend", instance.roles.get("backend", 0)),
            "frontend": validated_data.pop("frontend", instance.roles.get("frontend", 0)),
            "designer": validated_data.pop("designer", instance.roles.get("designer", 0)),
        }
        validated_data["roles"] = roles

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


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


# 비율형 모집글 상세 조회용 (선형님 전용)
class PostSimpleDetailSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(source='user', read_only=True)
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
<<<<<<< Updated upstream
            'title', 'content', 'category',
            'date', 'place_name', 'address',
            'latitude', 'longitude', 'max_people',
        ]


=======
            'id', 'title', 'content', 'category', 'date',
            'place_name', 'address', 'latitude', 'longitude',
            'is_closed', 'max_people', 'created_at', 'updated_at',
            'writer', 'img_url', 'roles'
        ]

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return request.build_absolute_uri('/media/posts/images/default.png')
>>>>>>> Stashed changes
