import peewee_async

from aiohttp import web, WSCloseCode
from aiohttp import web_protocol

import settings

from core.models import Room, User, Message
from core.base import db

from urls import routes


class ChatApplication(web.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_startup.append(self.startup)
        self.on_shutdown.append(self.shutdown)
        self.websockets = {}

    async def startup(self):
        db.init(**settings.DATABASE)
        # db.create_tables([Message])
        self.database = db
        self.database.set_allow_sync(False)
        self.objects = peewee_async.Manager(self.database)
        self.logger = settings.logger
        for route in routes:
            self.router.add_route(**route)

    async def shutdown(self):
        for wslist in self.websockets.values():
            for ws in wslist:
                await ws.close()
