from rest_framework import serializers
from .models import ChatMessage

class ChatRoomSerializer(serializers.Serializer):
    room_id = serializers.CharField()
    post_id = serializers.IntegerField(allow_null=True)
    post_title = serializers.CharField(allow_blank=True)
    latest_message = serializers.CharField(allow_blank=True)
    latest_time = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()
    participants = serializers.ListField(child=serializers.CharField())

class ChatMessageSerializer(serializers.ModelSerializer):
    # nickname 필드가 있으면 그걸, 없으면 username tkdyd
    nickname = serializers.SerializerMethodField()

    class Meta:
        model = ChatMessage
        fields = [
            'ChatMessage_id',
            'chat_user_id',
            'nickname',
            'content',
            'created_at',
        ]
    # noinspection PyMethodMayBeStatic
    def get_nickname(self, obj):
        user = obj.chat_user
        if hasattr(user, 'nickname') and user.nickname:
            return user.nickname
        return user.get_username()

class ChatMessageCreateSerializer(serializers.ModelSerializer):
    content = serializers.CharField()

    class Meta:
        model = ChatMessage
        fields = [
            'ChatMessage_id',
            'room_id',
            'chat_user_id',
            'content',
            'created_at',
        ]
        read_only_fields = ['ChatMessage_id', 'room_id', 'chat_user_id', 'created_at']


