from rest_framework import serializers
from .models import ChatMessage
from apps.posts.models import Post
from django.contrib.auth import get_user_model

class ChatRoomSerializer(serializers.Serializer):
    room_id = serializers.CharField()
    post_id = serializers.IntegerField(allow_null=True)
    post_title = serializers.CharField(allow_blank=True)
    latest_message = serializers.CharField(allow_blank=True)
    latest_time = serializers.DateTimeField(allow_null=True)
    unread_count = serializers.IntegerField()
    participants = serializers.ListField(child=serializers.CharField())
    title = serializers.SerializerMethodField()

    def get_title(self, obj):
        room_id = obj['room_id']
        User = get_user_model()
        if room_id.isdigit():
            try:
                post = Post.objects.get(id=int(room_id))
                return post.title
            except Post.DoesNotExist:
                return ''
        elif '_' in room_id:
            a, b = room_id.split('_', 1)
        else:
            return ''

        me = str(self.context['request'].user.id)
        other_id = b if a == me else a
        try:
            other = User.objects.get(id=other_id)
            return getattr(other, 'nickname', other.get_username())
        except User.DoesNotExist:
            return ''

    class Meta:
        fields = [
            'room_id',
            'title',
            'post_id',
            'post_title',
            'latest_message',
            'latest_time',
            'unread_count',
            'participants',
        ]

class ChatMessageSerializer(serializers.ModelSerializer):
    # nickname 필드와 프로필 이미지 URL
    nickname = serializers.SerializerMethodField()
    profile_image = serializers.SerializerMethodField()
    content = serializers.CharField()

    class Meta:
        model = ChatMessage
        fields = [
            'ChatMessage_id',
            'chat_user_id',
            'nickname',
            'profile_image',
            'content',
            'created_at',
        ]
    # noinspection PyMethodMayBeStatic
    def get_nickname(self, obj):
        user = obj.chat_user
        if hasattr(user, 'nickname') and user.nickname:
            return user.nickname
        return user.get_username()

    def get_profile_image(self, obj):
        user = obj.chat_user
        profile = getattr(user, 'profile_image', None) # 1) getattr 로 안전하게 꺼내고
        if hasattr(profile, 'url'): # 2) FileField / ImageField 인스턴스면 .url 반환
            return profile.url
        if isinstance(profile, str): # 3) 이미 문자열로 저장된 URL/경로라면 그대로 반환
            return profile
        return None # 4) 그 외(없거나 빈값)에는 None

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


