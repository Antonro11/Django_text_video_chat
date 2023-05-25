import json

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from account.models import Account
from app.consumers import get_user_pk, get_room, get_first_user_room, get_second_user_room


class MyConsumerList(AsyncWebsocketConsumer):
    async def connect(self):
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]
        await self.channel_layer.group_add("list-"+chat_room, self.channel_name)
        await self.accept()


    async def disconnect(self, close_code):
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]
        await self.channel_layer.group_discard("list-"+chat_room, self.channel_name)

    async def receive(self,text_data):
        chat_room = self.scope["url_route"]["kwargs"]["chat_room"]

        data = json.loads(text_data)

        if "video-call-clicked" in data.keys():
            await self.channel_layer.group_send("list-"+chat_room, {
                'type': 'video.call',
                "calling": data
            })

        if "update_from_room" in data.keys():
            update_from_room = data["update_from_room"]
            instance_chat =await get_room(update_from_room)
            first_account = await get_first_user_room(instance_chat.pk)
            second_account = await get_second_user_room(instance_chat.pk)

            for i in self.scope["headers"]:
                if "cookie" in i[0].decode():
                    session_id = i[-1].decode().split(";")[-1].split("=")[-1]
                    user_pk = await get_user_pk(session_id)
                    account = await sync_to_async(Account.objects.get)(pk=user_pk)

                    break

            await self.channel_layer.group_send("list-"+chat_room, {
                'type': 'chat.message',
                "update": [first_account.username,second_account.username]
            })

    async def chat_message(self, event):
        update = event["update"]
        await self.send(text_data=json.dumps({"update": update}))

    async def video_call(self, event):
        calling = event["calling"]
        await self.send(text_data=json.dumps({"calling": calling}))

    async def my_message_type(self, event):
        my_data = json.loads(event["data"])
        await self.send(text_data=json.dumps(my_data))



