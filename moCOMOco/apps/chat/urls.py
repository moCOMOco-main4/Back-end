from django.urls import path
from .views import ChatRoomListView, ChatMessageListView ,ChatMessageCreateView , ChatMessageDestroyView

urlpatterns =[
    path('<str:room_id>/messages/', ChatMessageListView.as_view(), name='chat-message-list'),
    path('rooms/', ChatRoomListView.as_view(), name='chat-room-list'),
    path('<str:room_id>/messages/send/', ChatMessageCreateView.as_view(), name='chat-message-create'),
    path('<str:room_id>/messages/<int:message_id>/', ChatMessageDestroyView.as_view(), name='chat-message-delete'),
]