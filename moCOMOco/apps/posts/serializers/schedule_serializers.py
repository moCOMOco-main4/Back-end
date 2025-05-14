from rest_framework import serializers
from apps.posts.models.schedule import Schedule


class ScheduleCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'post', 'date', 'description']


class ScheduleUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['date', 'description']


class ScheduleListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Schedule
        fields = ['id', 'post', 'date', 'description', 'created_at']
