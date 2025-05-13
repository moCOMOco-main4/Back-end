from rest_framework import serializers
from apps.posts.models.schedule import Schedule

# 일정 등록
class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date', 'memo', 'created_at']
        read_only_fields = ['created_at']


# 일정 수정
class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date', 'memo']
        read_only_fields = []
        extra_kwargs = {
            'date': {'required': False},
            'memo': {'required': False},
        }


# 일정 목록 조회
class ScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id','date', 'memo']
