from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from django.utils import timezone
from .models import ChatMessage, ChatRoomParticipant
from apps.notifications.services import NotificationService

class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.group_name = f'chat_{self.room_id}'

        # 참여자 권한 확인 (sync→async 래핑)
        #is_participant = await database_sync_to_async(
        #    lambda: ChatRoomParticipant.objects.filter(
        #        room_id=self.room_id,
        #        user=self.scope['user']
        #    ).exists()
        #)()
        #if not (self.scope['user'].is_authenticated and is_participant):
        #    # 인증 실패 시 연결 끊기
        #    await self.close()
        #    return

        # 그룹에 참가
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # 그룹에서 탈퇴
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        message_text = content.get('message', '').strip()
        if not message_text:
            return  # 빈 메시지는 무시

        user = self.scope['user']

        # 1) DB에 메시지 저장
        chat_msg = await database_sync_to_async(ChatMessage.objects.create)(
            room_id=self.room_id,
            chat_user=user,
            content=message_text
        )
        # 2) 알림 생성 (WS 메시지에도 NotificationService 호출)
        await database_sync_to_async(
            NotificationService.send_chat_message_notification
        )(chat_msg)

        # 그룹 전체에 브로드캐스트
        await self.channel_layer.group_send(
            self.group_name,
            {
                'type': 'chat_message',
                'message_id': chat_msg.ChatMessage_id,
                'user_id': chat_msg.chat_user.id,
                'nickname': chat_msg.chat_user.nickname,
                'message': chat_msg.content,
                'created_at': chat_msg.created_at.isoformat(),
            }
        )

    async def chat_message(self, event):
        # 그룹 메시지를 클라이언트에 전송
        await self.send_json({
            'message_id': event['message_id'],
            'chat_user_id': event['user_id'],
            'nickname': event['nickname'],
            'content': event['message'],
            'created_at': event['created_at'],
        })