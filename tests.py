import unittest
import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from core.models import Room
from server import ChatApplication

import main


class MyAppTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = await main.get_application()
        return app

    @unittest_run_loop
    async def test_room_create(self):
        resp = await self.client.request('POST', '/chat/rooms/')
        assert resp.status == 201

    @unittest_run_loop
    async def test_msg_sending(self):
        room = await self.app.objects.create(Room)
        ws1 = await self.client.ws_connect(f'/ws/{room.id}')
        ws2 = await self.client.ws_connect(f'/ws/{room.id}')

        text_to_send = 'test'
        await ws1.send_str(text_to_send)
        ack_msg2 = await ws2.receive()

        assert json.loads(ack_msg2.data)[0].get('text') == text_to_send
        room.delete()


if __name__ == '__main__':
    unittest.main()