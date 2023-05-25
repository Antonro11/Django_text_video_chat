import asyncio
import json

from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth import get_user, get_user_model
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer
from channels.middleware import BaseMiddleware
from django.contrib.sessions.models import Session
from django.http import HttpResponse

from account.models import Account
from app.models import PrivatMessage

from config.settings import BASE_DIR



@database_sync_to_async
def get_user_pk(session_id):
    session = Session.objects.get(session_key=session_id)
    user_id = session.get_decoded().get('_auth_user_id')
    if user_id is not None:
        user = get_user_model().objects.get(pk=user_id)
        return user.pk


@database_sync_to_async
def get_first_unread_user_room(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.unread_count_first_account

@database_sync_to_async
def get_second_unread_user_room(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.unread_count_second_account


@database_sync_to_async
def get_first_user_room(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.first_account

@database_sync_to_async
def get_second_user_room(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.second_account

@database_sync_to_async
def get_room(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room


@database_sync_to_async
def who_starts_stream(username,room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    room.who_start_stream = username
    return room.save()

@database_sync_to_async
def get_who_starts_stream(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.who_start_stream


@database_sync_to_async
def saving_instance(instance_model):
    return instance_model.save()


class ConsumerVideo(AsyncWebsocketConsumer):
    async def connect(self):

        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]

        await self.channel_layer.group_add("video-"+chat_room, self.channel_name)

        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]
                user_pk =await get_user_pk(session_id)
                account = await sync_to_async(Account.objects.get)(pk=user_pk)
                account.video_on = 1
                await saving_instance(account)
                break

        await self.accept()

    async def disconnect(self, close_code):
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]
        account_starts_stream=await get_who_starts_stream(chat_room)

        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]

                user_pk =await get_user_pk(session_id)
                account = await sync_to_async(Account.objects.get)(pk=user_pk)

                if account_starts_stream == str(account):
                    await who_starts_stream(None, chat_room)

                account.video_on = 0
                await saving_instance(account)
                break

        await self.channel_layer.group_discard("video-"+chat_room, self.channel_name)

    async def receive(self,text_data):

        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]

        data = json.loads(text_data)

        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]
                user_pk =await get_user_pk(session_id)
                account = await sync_to_async(Account.objects.get)(pk=user_pk)

                if "event" in data.keys():
                    if "turn_off_video" == data["event"]:
                        account.video_on = 0
                        await saving_instance(account)
                    elif "turn_on_video" == data["event"]:
                        account.video_on = 1
                        await saving_instance(account)

                break

        await self.channel_layer.group_send("video-"+chat_room, {
            'type': 'handle.video',
            "data": data
        })




    async def handle_video(self, event):
        data = event["data"]
        await self.send(text_data=json.dumps({"data": data}))


    async def send_ice_candidate(self, event):
        candidate = event["candidate"]
        await self.send(text_data=json.dumps({"candidate": candidate}))


    async def handle_message(self, event):
        data = event['message']
        await self.send(text_data=json.dumps({'message': data}))




class ConsumerCallingStatus(AsyncWebsocketConsumer):
    async def connect(self):
        calling_status_room = self.scope["url_route"]["kwargs"]["calling_status_room"]
        await self.channel_layer.group_add("calling-" + calling_status_room, self.channel_name)
        await self.accept()

    async def receive(self,text_data):
        calling_status_room = self.scope["url_route"]["kwargs"]["calling_status_room"]
        data = json.loads(text_data)

    async def disconnect(self, close_code):
        calling_status_room = self.scope["url_route"]["kwargs"]["calling_status_room"]
        await self.channel_layer.group_discard("calling-" + calling_status_room, self.channel_name)