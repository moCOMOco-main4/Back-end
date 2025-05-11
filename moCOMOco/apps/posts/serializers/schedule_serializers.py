from rest_framework import serializers
from apps.posts.models import Schedule
# 일정 생성
class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['post', 'date', 'memo']
#일정 리스트 조회
class ScheduleListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    type = serializers.SerializerMethodField()

    class Meta:
        model = Schedule
        fields = ['post_id', 'post_title', 'date', 'memo', 'type']

    def get_type(self, obj):
        user = self.context['request'].user
        if obj.post.user == user:
            return 'created'
        return 'participated'