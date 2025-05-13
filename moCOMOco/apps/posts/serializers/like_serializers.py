from rest_framework import serializers

# 단순 메시지 응답
class MessageSerializer(serializers.Serializer):
    message = serializers.CharField()
