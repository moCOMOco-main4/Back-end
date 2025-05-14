from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions , generics , status
from .models import ChatRoomParticipant, ChatMessage
from apps.posts.models import Post
from .serializers import ChatRoomSerializer , ChatMessageSerializer , ChatMessageCreateSerializer
from rest_framework.exceptions import PermissionDenied
from apps.notifications.services import NotificationService
from rest_framework.generics import GenericAPIView
from django.contrib.auth import get_user_model


class ChatRoomListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        room_ids = (
            ChatRoomParticipant.objects
            .filter(user=user)
            .values_list('room_id', flat=True)
            .distinct()
        )

        rooms = []
        for room_id in room_ids:
            participants_qs = (
                ChatRoomParticipant.objects
                .filter(room_id=room_id)
                .select_related('user')
            )
            # nickname 필드가 있으면 그걸, 없으면 username 사용
            nicknames = [
                getattr(p.user, 'nickname', p.user.get_username())
                for p in participants_qs
            ]

            latest = (
                ChatMessage.objects
                .filter(room_id=room_id, is_deleted=False)
                .order_by('-created_at')
                .first()
            )
            latest_message = latest.content if latest else ''
            latest_time = latest.created_at if latest else None

            unread_count = ChatMessage.objects.filter(
                room_id=room_id
            ).exclude(chat_user_id=user.id).count()
            try:
                post_pk = int(room_id.split('_',1)[0])
                post = get_object_or_404(Post, pk=post_pk)
                post_id = post.pk
                post_title = post.title
            except Exception:
                post_id = None
                post_title = ''


            rooms.append({
                'room_id': room_id,
                'post_id': post_id,
                'post_title': post_title,
                'latest_message': latest_message,
                'latest_time': latest_time,
                'unread_count': unread_count,
                'participants': nicknames,
            })

        serializer = ChatRoomSerializer(
            rooms,
            many=True,
            context={'request': request}
        )
        return Response(serializer.data)

class ChatMessageListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageSerializer

    def get_queryset(self):
        user = self.request.user
        room_id = self.kwargs['room_id']
        if not ChatRoomParticipant.objects.filter(user=user, room_id=room_id).exists():
            raise PermissionDenied(detail="해당 채팅방의 참여자가 아닙니다.")
        return(
            ChatMessage.objects
            .filter(room_id=room_id, is_deleted=False)
            .order_by('created_at')
        )

class ChatMessageCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ChatMessageCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        room_id = self.kwargs['room_id']

        if not ChatRoomParticipant.objects.filter(user=user, room_id=room_id).exists():
            raise PermissionDenied("해당 채팅방의 참여자가 아닙니다.")
        serializer.save(room_id=room_id, chat_user=user)
        message = serializer.save(room_id=room_id, chat_user=user) # 메시지를 저장하고 , 반환된 인스턴스를 변수에 받음
        NotificationService.send_chat_message_notification(message) # 저장된 메시지 정보로 알림을 자동 생성

    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

class ChatMessageDestroyView(generics.DestroyAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = ChatMessage.objects.all()
    lookup_field = 'ChatMessage_id'
    lookup_url_kwarg = 'message_id'

    def get_object(self):
        obj = super().get_object()
        user = self.request.user
        room_id = obj.room_id

        if not ChatRoomParticipant.objects.filter(user=user, room_id=room_id).exists():
            raise PermissionDenied("해당 채팅방의 참여자가 아닙니다.")

        if obj.chat_user_id != user.id:
            raise PermissionDenied("본인이 보낸 메시지만 삭제할 수 있습니다.")

        return obj

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save()


User = get_user_model()
class OneToOneChatRoomCreateView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        me = request.user
        other_id = request.data.get('other_user_id')
        if not other_id:
            return Response({"detail": "other_user_id가 필요합니다."},
                            status=status.HTTP_400_BAD_REQUEST)
        if int(other_id) == me.id:
            return Response({"detail": "자기 자신과는 채팅할 수 없습니다."},
                            status=status.HTTP_400_BAD_REQUEST)

        ids = sorted([me.id, int(other_id)])
        room_id = f"{ids[0]}_{ids[1]}"

        participants = [] # 두 사람 모두 참가자로 추가(중복을 방지하기 위해서 해놨음)
        for uid in ids:
            user = User.objects.get(id=uid)
            p, _ = ChatRoomParticipant.objects.get_or_create(
                user=user,
                room_id=room_id,
                defaults={'alarm_on': True}
            )
            participants.append(p)

        NotificationService.send_chat_join_notification(participants[1]) # 알림 : 상대방에게 "메시지 전송 준비" join 알림

        try:
            post_pk = int(room_id)
            post = Post.objects.get(pk=post_pk)
            post_id = post_pk
            post_title = post.title
        except ValueError:
            post_id = None
            post_title = ''
        except Post.DoesNotExist:
            post_id = None
            post_title = ''

        participants_qs = ChatRoomParticipant.objects.filter(room_id=room_id).select_related('user')
        nicknames_list = [
            getattr(p.user, 'nickname', p.user.get_username())
            for p in participants_qs
        ]
        room_meta = {
            'room_id': room_id,
            'post_id': post_id,
            'post_title': post_title,
            'latest_message': '',
            'latest_time': None,
            'unread_count': 0,
            'participants': nicknames_list,
        }
        serializer = ChatRoomSerializer(
            room_meta,
            context={'request': request}
        )
        return Response(serializer.data, status=status.HTTP_201_CREATED)

