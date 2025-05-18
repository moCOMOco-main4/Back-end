from rest_framework import serializers
from apps.posts.models.schedule import Schedule

class ScheduleCreateSerializer(serializers.ModelSerializer):
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
    post_date = serializers.SerializerMethodField()

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
            'post_title'
        ]

    def get_post_date(self, obj):
        return obj.post.date.strftime('%Y-%m-%d') if obj.post.date else None
