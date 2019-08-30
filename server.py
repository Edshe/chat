import asyncio
import json
import random
import peewee_async

import aioredis
from aiohttp import web, WSCloseCode

import settings

from core.models import db
from urls import routes


class ChatApplication(web.Application):

    def __init__(self, **kwargs):
        super(ChatApplication, self).__init__(**kwargs)

        # db conn
        db.init(**settings.DATABASE)
        self.database = db
        self.database.set_allow_sync(False)
        self.objects = peewee_async.Manager(self.database)

        self.websockets = {}
        self.logger = settings.logger

        self.loop.run_until_complete(self._setup())

    async def _setup(self):
        self.redis_pool = await aioredis.create_pool(
            (settings.REDIS_HOST, settings.REDIS_PORT),
            loop=self.loop
        )
        for route in routes:
            self.router.add_route(**route)
