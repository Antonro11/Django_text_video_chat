import json

from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from django.contrib.sessions.models import Session

from account.models import Account
from app.models import PrivatMessage, UnreadMessages

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
def get_messages(room_id):
    room = PrivatMessage.objects.get(pk=room_id)
    return room.messages

@database_sync_to_async
def saving_instance(instance_model):
    return instance_model.save()

@database_sync_to_async
def unread_messages(chat_room):
    instances_unread = UnreadMessages.objects.filter(room=chat_room)
    return [(i.pk, str(i.account),str(i.receiver_accounts)) for i in instances_unread]

@database_sync_to_async
def get_unread_messages(id):
    instances_unread = UnreadMessages.objects.get(pk=id)
    return instances_unread

@database_sync_to_async
def get_unread_username(id):
    unread_username = UnreadMessages.objects.get(pk=id).account.username
    return unread_username


class MyConsumer(AsyncWebsocketConsumer):
    async def connect(self):

        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]

        await self.channel_layer.group_add(chat_room, self.channel_name)
        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]

                user_pk = await get_user_pk(session_id)

                account = await sync_to_async(Account.objects.get)(pk=user_pk)
                first_account = await get_first_user_room(chat_room)
                room_instance = await get_room(chat_room)
                room_instance.connected_to_chat += account.username
                await saving_instance(room_instance)


                for i in await unread_messages(chat_room):
                    if account.username == i[1]:
                        instance_unread = await get_unread_messages(i[0])
                        instance_unread.count_unread = 0
                        await saving_instance(instance_unread)

                break


        await self.accept()


    async def disconnect(self, close_code):
        # Perform any cleanup you need for the consumer here
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]

        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]

                user_pk =await get_user_pk(session_id)

                account = await sync_to_async(Account.objects.get)(pk=user_pk)

                room_instance = await get_room(chat_room)
                on_room = room_instance.connected_to_chat
                new_on_room = on_room.replace(str(account.username), "")
                room_instance.connected_to_chat = new_on_room
                await saving_instance(room_instance)

                for i in await unread_messages(chat_room):
                    if account.username == i[1]:
                        instance_unread = await get_unread_messages(i[0])
                        instance_unread.count_unread = 0
                        await saving_instance(instance_unread)

                break

        # Remove the consumer from the group
        await self.channel_layer.group_discard(chat_room, self.channel_name)

    async def receive(self,text_data):
        # Handle incoming messages from the WebSocket here
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]
        chat_messages = get_messages(chat_room)
        path_to_messages = str(BASE_DIR) + str(await chat_messages)
        room_instance = await get_room(chat_room)

        for i in self.scope["headers"]:
            if "cookie" in i[0].decode():
                session_id = i[-1].decode().split(";")[-1].split("=")[-1]
                user_pk =await get_user_pk(session_id)
                account = await sync_to_async(Account.objects.get)(pk=user_pk)

                break


        data = json.loads(text_data)
        data_keys = [i for i in data.keys()]

        if "ws_opened" in data_keys:
            await self.channel_layer.group_send(chat_room, {
                'type': 'ws.opened',
                'ws_opened': data
            })

        if "reload_after_delete" in data_keys:
            await self.channel_layer.group_send(chat_room, {
                'type': 'handle.delete',
                'reload_after_delete': data
            })

        if "video-call-clicked" in data_keys:
            await self.channel_layer.group_send(chat_room, {
                'type': 'video.click',
                'video-clicked': data
            })

        if "text" in data_keys and account.username == data["user"]:
            with open(path_to_messages,"a") as txtfile:
                txtfile.write(data["user"]+ "__split__" +data["text"] + "\n")

            for i in await unread_messages(chat_room):
                if account.username != i[1]:

                    instance_unread = await get_unread_messages(i[0])
                    unread_username = await get_unread_username(i[0])
                    if unread_username not in room_instance.connected_to_chat:
                        instance_unread.count_unread += 1
                        await saving_instance(instance_unread)

            await self.channel_layer.group_send(chat_room, {
                'type': 'handle.message',
                'message': data
            })



    async def handle_message(self, event):
        data = event['message']
        await self.send(text_data=json.dumps({'message': data}))


    async def video_click(self, event):
        clicked = event['video-clicked']
        await self.send(text_data=json.dumps({'clicked': clicked}))

    async def handle_delete(self, event):
        data = event['reload_after_delete']
        await self.send(text_data=json.dumps({'reload_after_delete': data}))


    async def ws_opened(self, event):
        data = event['ws_opened']
        await self.send(text_data=json.dumps({'ws_opened': data}))

    async def handle_video(self, event):
        pass
