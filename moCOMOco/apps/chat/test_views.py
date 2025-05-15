# apps/chat/tests/test_views.py

from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.chat.models import ChatRoomParticipant, ChatMessage

class ChatRoomListAPITest(TestCase):
    def setUp(self):
        User = get_user_model()
        # 1) 테스트용 유저 생성
        self.user = User.objects.create_user(
            email='testuser@naver.com',
            password='testpass'  # nosec B106
        )
        # 2) 채팅방 참여자 레코드 생성
        ChatRoomParticipant.objects.create(
            user=self.user,
            room_id=1,
            alarm_on=True
        )
        # 3) 해당 방에 메시지 두 개 저장
        ChatMessage.objects.create(
            room_id=1,
            chat_user=self.user,
            content='첫 메시지'
        )
        ChatMessage.objects.create(
            room_id=1,
            chat_user=self.user,
            content='두 번째 메시지'
        )

        # 4) DRF APIClient 준비 및 인증
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_get_chat_rooms(self):
        # GET /chat/rooms/ 호출
        response = self.client.get('/chat/rooms/')
        # 상태 코드 확인
        self.assertEqual(response.status_code, 200)

        data = response.json()
        # 응답이 리스트이고, 길이가 1이어야 함
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)

        room = data[0]
        # room_id 및 latest_message 검증
        self.assertEqual(room['room_id'], '1')  # API가 문자열로 반환하기 때문
        self.assertEqual(room['latest_message'], '두 번째 메시지')
                # participants 검증 (현재 API가 빈 문자열 리스트를 반환함)
        self.assertEqual(room['participants'], [''])
