import psycopg2
from psycopg2 import sql

import logging.config
import unittest
import json
from aiohttp.test_utils import AioHTTPTestCase, unittest_run_loop

from chat.models import Room
from create_tables import create_tables
import settings
import app as application


class BaseChatTestCase(AioHTTPTestCase):

    async def get_application(self):
        app = await application.get_application()
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
        data = await resp.text()

        data = json.loads(data)
        count = len(await self.app.objects.execute(Room.select()))
        assert data.get('count') == count

    @unittest_run_loop
    async def test_room_retrieve(self):
        room = await self.app.objects.create(Room)
        resp = await self.client.request('GET', f'/chat/rooms/{room.id}/')
        assert resp.status == 200


class MessageAPITestCase(BaseChatTestCase):

    @unittest_run_loop
    async def test_msg_sending(self):
        room = await self.app.objects.create(Room)
        ws1 = await self.client.ws_connect(f'/ws/{room.id}/')
        ws2 = await self.client.ws_connect(f'/ws/{room.id}/')

        text_to_send = 'test'
        await ws1.send_str(text_to_send)
        msg = await ws2.receive()

        assert json.loads(msg.data).get('results')[0].get('text') == text_to_send
        room.delete()


if __name__ == '__main__':

    settings.DATABASE['database'] += '_test'

    con = psycopg2.connect(
        dbname='postgres',
        user=settings.DATABASE['user'],
        password=settings.DATABASE['password'],
        host=settings.DATABASE['host'],
        port=settings.DATABASE['port']
    )
    con.set_isolation_level(
        psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT
    )
    cur = con.cursor()

    try:
        cur.execute(sql.SQL(f"CREATE DATABASE {settings.DATABASE['database']}"))
        create_tables()
    except:
        pass


    logging.config.dictConfig(settings.LOGGING)

    try:
        unittest.main()
    except:
        pass

    cur.execute(sql.SQL(f"DROP DATABASE {settings.DATABASE['database']}"))