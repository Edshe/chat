from typing import Callable

from aiohttp.web_request import Request
from aiohttp.web_exceptions import HTTPMethodNotAllowed
from aiohttp import web


class BaseRESTView(web.View):

    DEFAULT_METHODS = ('get', 'post', 'put', 'delete', 'patch')

    def __init__(self):
        self.__methods = {}

        for name in self.DEFAULT_METHODS:
            method = getattr(self, name.lower(), None)
            if method:
                self._register_method(name, method)

    def _register_method(self, name: str, method: Callable):
        self.__methods[name] = method


    async def dispatch(self, request: Request):
        method = self.__methods.get(request.method)
        if not method:
            raise HTTPMethodNotAllowed(self.DEFAULT_METHODS)

        return await method()