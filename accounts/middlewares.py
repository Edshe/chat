from rest_framework.authentication import TokenAuthentication
from aiohttp.web import middleware


@middleware
async def toke_authentication(request, handler):

    auth = TokenAuthentication(self.request)
