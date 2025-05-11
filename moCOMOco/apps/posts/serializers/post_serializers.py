from rest_framework import serializers
from apps.posts.models import Post, Application
from apps.posts.serializers.application_serializers import ApplicationSimpleSerializer


# 모집글 생성 시리얼라이저
class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'roles', 'date', 'image'
        ]


# 모집글 리스트용 (홈 화면)
class PostListSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    image = serializers.ImageField(read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'category', 'place_name', 'is_closed', 'username', 'image']


# 모집글 상세 조회용
class PostDetailSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    applications = ApplicationSimpleSerializer(many=True, read_only=True)
    remaining_roles = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = [
            'id', 'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'roles', 'remaining_roles',
            'date', 'is_closed', 'created_at', 'updated_at',
            'image', 'username',  # user 필드 제거
            'applications'
        ]

    def get_remaining_roles(self, obj):
        """
        roles 필드 기반으로 각 역할에 남은 인원 계산
        예: {'backend': 1, 'frontend': 0}
        """
        result = {}
        for role, max_count in obj.roles.items():
            current = Application.objects.filter(post=obj, role=role).count()
            result[role] = max(0, max_count - current)
        return result


# 모집글 수정용
class PostUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = [
            'title', 'content', 'category',
            'place_name', 'address', 'latitude', 'longitude',
            'roles', 'date', 'image', 'is_closed'
        ]


# 지도 전용
class PostLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'place_name', 'latitude', 'longitude']
