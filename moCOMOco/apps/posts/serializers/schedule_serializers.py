from rest_framework import serializers
from apps.posts.models.schedule import Schedule
from datetime import datetime

class ScheduleCreateSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()

    def to_internal_value(self, data):
        if 'date' in data and isinstance(data['date'], str):
            try:
                # 예: "2025-05-20" → "2025-05-20T00:00:00" 으로 처리
                if len(data['date']) == 10:
                    data['date'] = data['date'] + 'T00:00:00'
            except Exception:
                pass  # 나중에 DRF validation이 처리하게 둠
        return super().to_internal_value(data)

    class Meta:
        model = Schedule
        fields = ['id', 'date', 'memo']



class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date', 'memo']


class ScheduleListSerializer(serializers.ModelSerializer):
    post_id = serializers.IntegerField(source='post.id', read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    post_date = serializers.DateTimeField(source='post.date', read_only=True, required=False)

    class Meta:
        model = Schedule
        fields = [
            'id',
            'post',
            'date',
            'memo',
            'created_at',
            'post_id',
            'post_date',
            'post_title',
        ]
