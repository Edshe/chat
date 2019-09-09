from typing import Callable
import peewee as models
import peewee_async

from aiohttp.web_request import Request
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp import web




class BaseRESTView(web.View):

    DEFAULT_METHODS = ('get', 'post', 'put', 'delete', 'patch')

    def __init__(self, request):
        self
        self._request = request

        self.__methods = {}
        for name in self.DEFAULT_METHODS:
            method = getattr(self, name, None)
            if method:
                self._register_method(name, method)

    def _register_method(self, name: str, method: Callable):
        self.__methods[name] = method

    async def dispatch(self, request: Request):
        method = self.__methods.get(request.method)
        if not method:
            raise HTTPMethodNotAllowed(self.DEFAULT_METHODS)

        return await method()





db = peewee_async.PostgresqlDatabase(None)

class BaseModel(models.Model):
    class Meta:
        database = db