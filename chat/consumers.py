import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync

from channels.generic.websocket import AsyncWebsocketConsumer

class TestConsumer(WebsocketConsumer):    #===> bu class admindan malumot kritganda  websocket urlga kritilgan  ma'lumot yuborish

    #ws: //
    def connect(self):
        self.room_name = "test_consumer"
        self.room_group_name = "test_consumer_group"
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(text_data=json.dumps({"status": "connected from django channels"}))

    # user_id, message
    def receive(self, text_data):
        print('=======', text_data, '=======')
        self.send(text_data=json.dumps({"status": "we got you"}))

    def disconnect(self, *args, **kwargs):
        print('--------disconnect---------')


    def send_notification(self, event):
        print(event.get('value'))
        data = json.loads(event.get('value'))
        self.send(text_data=json.dumps({"notification": data}))


class NewConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'new_consumer'
        self.room_group_name = "new_consumer_group"         #new_consumer_group ===> bu views dagi await new_consumer_group

        await(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        await self.send(text_data=json.dumps({"status": "connected from new async json consumer"}))

    async def receive(self, text_data):
        print('=======', text_data, '=======')
        await self.send(text_data=json.dumps({"status": "we got you"}))

    async def disconnect(self, *args, **kwargs):
        print('--------disconnect---------')


    async def send_notification(self, event):
        print(event.get('value'))
        data = json.loads(event.get('value'))
        await self.send(text_data=json.dumps({"notification": data}))



