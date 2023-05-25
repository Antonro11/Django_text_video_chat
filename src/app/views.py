import csv
import json
import os

from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.decorators import method_decorator
from django.utils.translation import gettext as _

from django.core.files.base import ContentFile, File

from channels.layers import get_channel_layer
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.decorators import gzip
from django.views.decorators.cache import cache_control
from django.views.decorators.csrf import csrf_exempt

from django.views.generic import ListView

from account.models import Account
from app.models import PrivatMessage, UnreadMessages
from config.settings import BASE_DIR


def index(request):
    channel_layer = get_channel_layer()
    print(channel_layer)
    print(request.GET.get("account"))
    return render(request, "index.html",{"account":request.user.username})

@csrf_exempt
def chat_room(request,chat_room):
    chat_instance = PrivatMessage.objects.get(id=str(chat_room))

    if request.method == "POST":
        print("Request Body:", request.body)
        if "delete_index" in str(request.body):
            print("Request Body:", request.body)
            data_json = json.loads(str(request.body)[2:-1])
            print("Request POST:", data_json["delete_index"])

            path_messages_file = f"{BASE_DIR}{chat_instance.messages}"
            with open(path_messages_file, "r") as file_messages:
                all_messages = file_messages.readlines()
                all_messages.pop(data_json["delete_index"])

            with open(path_messages_file, "w") as file_messages:
                file_messages.writelines(all_messages)

            print("AllMessagesDelete", all_messages)

            return render(request, "chat_room.html", {
                "chat_instance": chat_instance,
                "all_messages": all_messages
            })


    if request.POST.get("video-call"):
        instance = PrivatMessage.objects.get(pk=chat_room)
        instance.who_start_stream = request.POST.get("video-call").split()[1]
        instance.save()
        return HttpResponseRedirect(reverse_lazy("app:video-chat", kwargs={"video_chat_room": request.POST.get("video-call").split()[0]}))


   # if request.method=="POST" and not request.POST.get("video-call"):
    path_messages_file = str(BASE_DIR)+str(chat_instance.messages)
    with open(path_messages_file,"r") as txtfile:
        all_messages = txtfile.readlines()
        print("All messages", all_messages)

    return render(request, "chat_room.html",{
                                             "chat_instance":chat_instance,
                                             "all_messages": all_messages
                                             })

@method_decorator(cache_control(no_cache=True, must_revalidate=True, no_store=True), name='dispatch')
class ListUsers(ListView):
    template_name = "list_users.html"
    model = Account

    def post(self, request):
        if request.POST.get("message"):
            user = request.user.username
            receiver_user = request.POST.get("message")
            folder_messages = os.listdir(str(BASE_DIR) + "/static/messages/")
            print("sender, receiver", user, receiver_user)
            for messages_file in folder_messages:
                if user in messages_file and receiver_user in messages_file:
                    chat_instance_path = "/static/messages/" + messages_file
                    chat_instance = PrivatMessage.objects.get(messages=chat_instance_path)
                    return HttpResponseRedirect(reverse_lazy("app:chat-room", kwargs={"chat_room": chat_instance.pk}))


            file_chat_path = f"/static/messages/{user}_{receiver_user}.txt"
            chat_instance_path = f"{BASE_DIR}/static/messages/{user}_{receiver_user}.txt"
            with open(chat_instance_path, 'w') as txtfile:
                txtfile.write("")

            chat_instance = PrivatMessage.objects.create(
                messages=file_chat_path,
                first_account=Account.objects.get(username=user),
                second_account=Account.objects.get(username=receiver_user)
            )

            unread_instance_user = UnreadMessages.objects.create(
                account=Account.objects.get(username=user),
                receiver_accounts = Account.objects.get(username=receiver_user),
                room=chat_instance,
                count_unread=0
            )

            unread_instance_receiver = UnreadMessages.objects.create(
                account=Account.objects.get(username=receiver_user),
                receiver_accounts=Account.objects.get(username=user),
                room=chat_instance,
                count_unread=0
            )

            return HttpResponseRedirect(reverse_lazy("app:chat-room", kwargs={"chat_room": chat_instance.pk}))

    def get(self, request, *args, **kwargs):
        self.extra_context = {"all_unread": UnreadMessages.objects.all()}
        return super().get(request, *args, **kwargs)


def video_chat(request,video_chat_room):
    instance_video_chat_room = PrivatMessage.objects.get(pk=video_chat_room)
    return render(request, "video_chat.html",{"video_chat_room":instance_video_chat_room})


def calling_status(request, calling_status_room, user_calling):
    return render(request, "calling_status.html", {"calling_status_room":calling_status_room,"user_calling": user_calling})