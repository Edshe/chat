import re
import aiohttp_jinja2

from textwrap import dedent
from aiohttp import web, WSMsgType
from aiohttp.web_response import Response

from .models import Room, Message, User
from .utils import redirect, get_object_or_404
from .base import BaseRESTView
from .serializers import JSONModelSerializer



class RoomView(BaseRESTView):
    """
    View returns all rooms in JSON format
    """
    async def get(self) -> Response:
        rooms = await Room.all_rooms(self.request.app.objects)
        data = JSONModelSerializer(rooms).to_json()
        return web.json_response(data)

    async def post(self) -> Response:
        room = await self.request.app.objects.create(Room)

        data = await JSONModelSerializer(room).to_json()
        return web.json_response(data, status=201)


class WebSocket(BaseRESTView):
    """
    View processes WS connections
    for sending and retrieving new messages
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = self.request.app
        self.logger = self.app.logger

    async def get(self):
        ws = web.WebSocketResponse()
        await ws.prepare(self.request)
        self.ws_id = id(ws)

        # getting room by id
        self.room = await get_object_or_404(
            self.request,
            Room,
            id=self.request.match_info['slug']
        )
        # getting user by id
        # user = await self.request.app.objects.get(
        #     User,
        #     id=self.request.match_info['room']
        # )

        if self.room.id not in self.app.websockets:
            self.app.websockets[self.room.id] = {}

        self.app.websockets[self.room.id][self.ws_id] = ws

        async for msg in ws:
            print(msg.data)
            if msg.type == WSMsgType.TEXT:
                text = msg.data.strip()
                message = await self.request.app.objects.create(Message, room=self.room, user=None, text=text)
                await self.send_message(message)

            elif msg.type == WSMsgType.ERROR:
                self.app.logger.debug(f'Connection closed with exception {ws.exception()}')

        await self.disconnect(self.room.id, self.ws_id)

        return ws

    async def send_message(self, message):
        """
        Send messages to all in this room
        """
        print(self.app.websockets[self.room.id])
        for peer in self.app.websockets[self.room.id].values():
            await peer.send_json(await JSONModelSerializer(message).to_json())

    async def disconnect(self, room, ws):
        """
        Close connection and notify broadcast
        """
        socket = self.app.websockets[room].pop(ws)

        await socket.close()
