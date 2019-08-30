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


class WebSocket(BaseRESTView):
    """
    View processes WS connections
    for sending and retrieving new messages
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.app = self.request.app
        self.logger = self.app.logger

    async def get(self, request):
        # getting room by id
        self.room = await get_object_or_404(
            self.request,
            Room,
            id=self.request.match_info['room']
        )
        # getting user by id
        user = await self.request.app.objects.get(
            User,
            id=self.request.match_info['room']
        )

        ws = web.WebSocketResponse()
        await ws.prepare(self.request)

        if self.room.id not in request.app.wslist:
            self.app.websockets[self.room.id] = {}

        self.app.websockets[self.room.id][user.email] = ws

        async for msg in ws:
            if msg.tp == WSMsgType.TEXT:
                text = msg.data.strip()
                message = await request.app.objects.create(Message, room=self.room, user=user, text=text)
                await self.send_message(message)

            elif msg.tp == WSMsgType.ERROR:
                self.app.logger.debug(f'Connection closed with exception {ws.exception()}')

        return ws

    async def send_message(self, message):
        """
        Send messages to all in this room
        """
        for peer in self.request.app.websockets[self.room.id].values():
            peer.send_json(JSONModelSerializer(message))

    async def disconnect(self, username, socket, silent=False):
        """
        Close connection and notify broadcast
        """
        app = self.request.app
        app.websockets.pop(username, None)

        if not socket.closed:
            await socket.close()
        if silent:
            return
