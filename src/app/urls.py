
from django.urls import path

from app.views import index, chat_room, video_chat, calling_status

app_name = "app"

urlpatterns = [
    path("", index, name="index"),
    path("chat/<str:chat_room>/", chat_room, name="chat-room"),
    path("video-chat/<str:video_chat_room>/", video_chat, name="video-chat"),
    path("calling-status/<str:calling_status_room>/<str:user_calling>/", calling_status, name="calling_status")
]


