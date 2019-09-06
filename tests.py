import logging.config

import unittest
import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

import settings
from core.models import Room
from server import ChatApplication
import main


class BaseChatTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = await main.get_application()
        return app


class RoomAPITestCase(BaseChatTestCase):

    @unittest_run_loop
    async def test_room_create(self):
        resp = await self.client.request('POST', '/chat/rooms/')
        assert resp.status == 201

    @unittest_run_loop
    async def test_room_list(self):
        await self.app.objects.create(Room)
        resp = await self.client.request('GET', '/chat/rooms/')
        assert resp.status == 200

        data = json.loads(await resp.text())
        assert data.get('count') == 1

    @unittest_run_loop
    async def test_room_retrieve(self):
        room = await self.app.objects.create(Room)
        resp = await self.client.request('GET', '/chat/rooms/')
        assert resp.status == 200


class MessageAPITestCase(BaseChatTestCase):

    @unittest_run_loop
    async def test_msg_sending(self):
        room = await self.app.objects.create(Room)
        ws1 = await self.client.ws_connect(f'/ws/{room.id}')
        ws2 = await self.client.ws_connect(f'/ws/{room.id}')

        text_to_send = 'test'
        await ws1.send_str(text_to_send)
        msg = await ws2.receive()

        assert json.loads(msg.data).get('results')[0].get('text') == text_to_send
        room.delete()


if __name__ == '__main__':
    logging.config.dictConfig(settings.LOGGING)
    unittest.main()