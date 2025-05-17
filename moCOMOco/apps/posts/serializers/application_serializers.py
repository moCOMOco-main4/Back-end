from rest_framework import serializers
from apps.posts.models.application import Application
from apps.posts.models.post import Post
from apps.app_users.models import User


# 신청 생성용
class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ['role']

    def validate(self, data):
        user = self.context['request'].user
        post = self.context['post']
        role = data['role']

        # 자기글 자기 신청 못함
        if post.user == user:
            raise serializers.ValidationError("자신의 글에 신청 할수 없습니다.")

        # 마감 여부 확인
        if post.is_closed:
            raise serializers.ValidationError("이미 마감된 모집글입니다.")

        # 중복 신청 확인
        if Application.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("이미 신청한 모집글입니다.")

        # 해당 역할 존재 여부
        if role not in post.roles:
            raise serializers.ValidationError(f"{role} 역할은 이 모집글에 없습니다.")

        # 인원 초과 여부
        max_count = post.roles.get(role, 0)

        # 모집인원 0이면 신청 불가
        if max_count == 0:
            raise serializers.ValidationError(f'{role} 역할은 모집하지 않습니다.')

        # 연원 넘었는지 확인
        current_count = Application.objects.filter(post=post, role=role).count()

        if post.writer_role == role:
            current_count += 1

        if current_count >= max_count:
            raise serializers.ValidationError(f"{role} 역할 인원이 모두 찼습니다.")

        return data


# 간단 조회용 (내가 신청한 목록 등)
class ApplicationSimpleSerializer(serializers.ModelSerializer):
    post_title = serializers.CharField(source='post.title', read_only=True)
    role = serializers.CharField()

    class Meta:
        model = Application
        fields = ['id', 'post', 'post_title', 'role', 'created_at']


# 마이페이지 등에서 내가 신청한 글 전체 조회
class MyApplicationSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source='post.title')
    category = serializers.CharField(source='post.category')
    date = serializers.DateTimeField(source='post.date')
    place_name = serializers.CharField(source='post.place_name')
    is_closed = serializers.BooleanField(source='post.is_closed')
    role = serializers.CharField()

    class Meta:
        model = Application
        fields = ['id', 'title', 'category', 'date', 'place_name', 'role', 'is_closed']
