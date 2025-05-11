from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions , generics , status
from .models import ChatRoomParticipant, ChatMessage
#from apps.posts.models import Post
from .serializers import ChatRoomSerializer , ChatMessageSerializer , ChatMessageCreateSerializer
from rest_framework.exceptions import PermissionDenied


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
                getattr(p.user, 'nickname', p.user.username)
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

            '''
            try:
                post_pk = int(room_id.split('_',1)[0])
                post = get_object_or_404(Post, pk=post_pk)
                post_id = post.pk
                post_title = post.title
            except Exception:
                post_id = None
                post_title = ''
            '''

            post_id = None #포스트 앱 준비되면 위에 주석 해제하고 이 코드 주석처리
            post_title = '' #포스트 앱 준비되면 위에 주석 해제하고 이 코드 주석처리


            rooms.append({
                'room_id': room_id,
                'post_id': post_id,
                'post_title': post_title,
                'latest_message': latest_message,
                'latest_time': latest_time,
                'unread_count': unread_count,
                'participants': nicknames,
            })

        serializer = ChatRoomSerializer(rooms, many=True)
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

