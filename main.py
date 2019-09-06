import logging

import asyncio
from aiohttp import web
from aiohttp import web_app
import aiohttp_debugtoolbar
from server import ChatApplication
import settings


async def get_application(loop: object = None) -> object:
    """
    Function creates app instance
    and returns it
    """

    app = ChatApplication(
        loop=loop,
        logger=logging.getLogger('Chat')
    )

    return app


def main():
    app = get_application()
    web.run_app(app)


if __name__ == '__main__':
    main()