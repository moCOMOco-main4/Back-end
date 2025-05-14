from apps.notifications.models import Notification
from apps.chat.models import ChatRoomParticipant
from django.utils import timezone

class NotificationService:
    @staticmethod
    def send_chat_message_notification(message): # 채팅 메시지 생성 직후 호출. room_id의 다른 참가자들에게 알림을 보낸다.
        participants = ChatRoomParticipant.objects.filter(
            room_id=message.room_id
        ).exclude(user=message.chat_user)

        for p in participants:
            Notification.objects.create(
                user=p.user,
                chat_message=message,
                participant=p,
                type='chat_message',
                content=f"{message.chat_user.get_username()}님이 새 메시지를 보냈습니다.",
                url=f"/chat/{message.room_id}/message/",
                is_read=False,
                created_at=timezone.now()
            )

    @staticmethod
    def send_chat_join_notification(participant): # ChatRoomParticipant 생성 시(or입장 시) 호출. 기존 참가자들에게 누가 들어왔는지 알려줌.
        others = ChatRoomParticipant.objects.filter(
            room_id=participant.room_id
        ).exclude(pk=participant.pk)

        for p in others:
            Notification.objects.create(
                user=p.user,
                participant=participant,
                chat_message=None,
                type='chat_join',
                content=f"{participant.user.get_username()}님이 방에 참여했습니다.",
                url=f"/chat/{participant.room_id}/",
                is_read=False,
                created_at=timezone.now()
            )

    @staticmethod
    def send_chat_leave_notification(participant): # ChatRoomParticipant 삭제 시(or퇴장 시) 호출. 남은 참가자들에게 누가 나갔는지 알려줌.
        others = ChatRoomParticipant.objects.filter(
            room_id=participant.room_id
        )
        for p in others:
            Notification.objects.create(
                user=p.user,
                participant=participant,
                chat_message=None,
                type='chat_leave',
                content=f"{participant.user.get_username()}님이 방을 나갔습니다.",
                url=f"/chat/{participant.room_id}/",
                is_read=False,
                created_at=timezone.now()
            )

    @staticmethod
    def send_apply_created(application): # 새 신청이 생성된 직후에 Post 작성자에게 알림 보냄
        post_owner = application.post.user
        Notification.objects.create(
            user=post_owner,
            post=application.post,
            application=application,
            type='apply_created',
            content=f"{application.user.get_username()}님이 모임에 신청했습니다.",
            url=f"/posts/{application.post.id}/applications/",
            is_read=False,
            created_at=timezone.now()
        )

    @staticmethod
    def send_apply_accepted(application): # 신청이 수락된 직후, 신청자에게 알림 보냄
        Notification.objects.create(
            user=application.user,
            post=application.post,
            application=application,
            type='apply_accepted',
            content=f"{application.post.user.get_username()}님이 당신의 신청을 수락했습니다.",
            url=f"/posts/{application.post.id}/applications/{application.id}/",
            is_read=False,
            created_at=timezone.now()
        )

    @staticmethod
    def send_apply_rejected(application): # 신청이 거절된 직후, 신청자에게 알림 보냄
        Notification.objects.create(
            user=application.user,
            post=application.post,
            application=application,
            type='apply_rejected',
            content=f"{application.post.user.get_username()}님이 당신의 신청을 거절했습니다.",
            url=f"/posts/{application.post.id}/applications/{application.id}/",
            is_read=False,
            created_at=timezone.now()
        )

    @staticmethod
    def send_schedule_created(schedule): # Schedule이 생성된 직후 호출되어 Post작성자에게 알림을 보냄
        post = schedule.post
        Notification.objects.create(
            user=post.user,
            post=post,
            schedule=schedule,
            type='schedule_created',
            content=f"새 모임 일정이 등록되었습니다: {schedule.date}",
            url=f"/posts/{post.id}/schedules/",
            is_read=False,
            created_at=timezone.now()
        )

    @staticmethod
    def create_notification(*, to, notification_type, link, chat_message=None, post=None, schedule=None, application=None, participant=None):
        if notification_type == 'chat_join' and participant:
            content = f"{participant.user.get_username()}님이 방에 참여했습니다." # 1:1 채팅 입장 알림
        elif chat_message:
            content = chat_message.content # 일반 채팅 메시지 알림
        else:
            content = "새로운 알림이 도착했습니다." # 그 외(예: post, schedule 등) 알림

        return Notification.objects.create(
            user=to,
            chat_message=chat_message,
            post=post,
            schedule=schedule,
            application=application,
            participant=participant,
            type=notification_type,
            content=content,
            url=link,
            is_read=False,
            created_at=timezone.now()
        )