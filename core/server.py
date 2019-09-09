import logging

import peewee_async
from aiohttp import web

import settings
from core.base import db
from urls import routes


logger = logging.getLogger('Chat')


class ChatApplication(web.Application):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.logger = kwargs.get('logger')
        self.on_startup.append(self._set_db)
        self.on_startup.append(self._set_router)
        self.on_shutdown.append(self._close_sockets)
        self.websockets = {}

    async def _set_db(self, *args, **kawgs):
        logger.info('Setting up db')
        db.init(**settings.DATABASE)
        self.database = db
        self.database.set_allow_sync(False)
        self.objects = peewee_async.Manager(self.database)

    async def _set_router(self, *args, **kawgs):
        logger.info('Setting up routers')
        for route in routes:
            self.router.add_route(**route)

    async def _close_sockets(self, *args, **kawgs):
        logger.info('Closing users sockets')
        await db.close_async()
        for wslist in self.websockets.values():
            for ws in wslist:
                await ws.close()
