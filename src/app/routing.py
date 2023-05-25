from django.urls import path
from . import consumers, consumers_list, consumers_video

websocket_urlpatterns = [
    path('ws/chat/<str:chat_room>/', consumers.MyConsumer.as_asgi()),
    path('ws/list/<str:chat_room>/', consumers_list.MyConsumerList.as_asgi()),
    path('ws/video-chat/<str:chat_room>/', consumers_video.ConsumerVideo.as_asgi()),
    path('ws/calling-status/<str:calling_status_room>/<str:user_calling>/', consumers_video.ConsumerCallingStatus.as_asgi())
]
