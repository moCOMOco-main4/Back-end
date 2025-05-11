from rest_framework import serializers
from apps.posts.models import Application


# 신청자 리스트 시리얼라이저 (내 글에 신청한 사용자용)
class ApplicationSimpleSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'username', 'role', 'created_at', 'status']


# 내가 신청한 모집글 목록용
class MyApplicationSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'post_id', 'post_title', 'role', 'created_at', 'status']


# 신청 생성용
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['post', 'role']
        # user, created_at, status는 view 또는 model에서 처리됨

# 수락 거절
class ApplicationStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['status']
        extra_kwargs = {
            'status' : {
                'read_only': False,
                'help_text' : "'accepted' or 'rejected' 중 하나만 선택"
            }
        }

        def validate_state(self, value):
            if value not in ['accepted', 'rejected']:
                raise serializers.ValidationError("상태는 'accepted' or 'rejected' 만 가능")
            return value