from rest_framework import serializers

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
        example=2
    )
    frontend = serializers.IntegerField(
        required=False,
        default=0,
        help_text="프론트엔드 모집 인원 수",
        example=1
    )
    designer = serializers.IntegerField(
        required=False,
        default=0,
        help_text="디자이너 모집 인원 수",
        example=1
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

    # 프론트에서 역할군 개별 입력
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
        # 역할 필드 분리해서 dict로 조합
        roles = {
            "backend": validated_data.pop("backend", instance.roles.get("backend", 0)),
            "frontend": validated_data.pop("frontend", instance.roles.get("frontend", 0)),
            "designer": validated_data.pop("designer", instance.roles.get("designer", 0)),
        }
        validated_data["roles"] = roles

        # 나머지 필드 업데이트
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance


# 모집글 목록 조회용
class PostListSerializer(serializers.ModelSerializer):
    is_liked = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'category', 'is_closed', 'date',
            'place_name', 'latitude', 'longitude', 'max_people',
            'is_liked', 'img_url'
        ]

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

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


# 모집글 상세 조회
class PostDetailSerializer(serializers.ModelSerializer):
    writer = WriterSerializer(source='user', read_only=True)
    participants = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()
    is_applied = serializers.SerializerMethodField()
    img_url = serializers.SerializerMethodField()
    current_people = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category', 'date',
            'place_name', 'address', 'latitude', 'longitude',
            'is_closed', 'max_people', 'created_at', 'updated_at',
            'writer', 'participants', 'is_liked', 'is_applied',
            'img_url', 'current_people'
        ]

    def get_participants(self, obj):
        applications = Application.objects.filter(post=obj)
        return ParticipantSerializer(applications, many=True).data

    def get_is_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return PostLike.objects.filter(post=obj, user=user).exists()
        return False

    def get_is_applied(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return Application.objects.filter(post=obj, user=user).exists()
        return False

    def get_img_url(self, obj):
        request = self.context.get('request')
        if obj.image:
            return request.build_absolute_uri(obj.image.url)
        return request.build_absolute_uri('/media/posts/images/default.png')

    def get_current_people(self, obj):
        return Application.objects.filter(post=obj).count()


# 모집글 수정
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'date', 'place_name', 'address', 'latitude', 'longitude', 'max_people']
        extra_kwargs = {field: {'required': False} for field in fields}