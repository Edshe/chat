import aiohttp_debugtoolbar
from server import ChatApplication

import settings

middlewares = []

if settings.DEBUG:
    middlewares.append(aiohttp_debugtoolbar.middleware)

# init application
app = ChatApplication(
    middlewares=middlewares
)



