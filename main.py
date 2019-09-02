import asyncio
from aiohttp import web
from aiohttp import web_app
import aiohttp_debugtoolbar
from server import ChatApplication
import settings


middlewares = []

# if settings.DEBUG:
#     middlewares.append(aiohttp_debugtoolbar.middleware)


async def get_application(loop=None):
    """
    Function creates app instance
    and returns it
    """
    app = ChatApplication(
        loop=loop
    )
    return app


def main():
    app = get_application()
    web.run_app(app)


if __name__ == '__main__':
    main()