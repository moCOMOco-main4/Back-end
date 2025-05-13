from rest_framework import serializers
from apps import Application

# 모집 신청 생성용
class ApplicationCreateSerializer(serializers.ModelSerializer):
    role = serializers.CharField()

    class Meta:
        model = Application
        fields = ['role']  # user, post는 view에서 context로 전달됨

    def validate(self, attrs):
        role = attrs['role']
        user = self.context['request'].user
        post = self.context['post']

        if post.is_closed:
            raise serializers.ValidationError("모집이 마감된 글입니다.")
        if role not in post.roles:
            raise serializers.ValidationError(f"{role} 역할은 존재하지 않습니다.")

        max_count = post.roles[role]
        current_count = Application.objects.filter(post=post, role=role).count()
        if current_count >= max_count:
            raise serializers.ValidationError(f"{role} 역할은 이미 마감되었습니다.")

        if Application.objects.filter(user=user, post=post).exists():
            raise serializers.ValidationError("이미 신청하셨습니다.")

        return attrs

    def create(self, validated_data):
        user = self.context['request'].user
        post = self.context['post']
        role = validated_data['role']
        return Application.objects.create(user=user, post=post, role=role)


# 내가 신청한 글 목록 조회
class MyApplicationSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id')
    title = serializers.CharField(source='post.title')
    category = serializers.CharField(source='post.category')
    is_closed = serializers.BooleanField(source='post.is_closed')
    date = serializers.DateTimeField(source='post.date')
    place_name = serializers.CharField(source='post.place_name')
    role = serializers.CharField()

    class Meta:
        model = Application
        fields = [
            'post_id', 'title', 'category', 'date', 'place_name',
            'role', 'is_closed', 'created_at',
        ]
