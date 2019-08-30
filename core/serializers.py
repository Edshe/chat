import asyncio
from typing import Iterable


class JSONModelSerializer:

    def __init__(self, objects):
        if isinstance(objects, Iterable):
            self.objects = objects
        else:
            self.objects = [objects, ]

    async def to_json(self):
        result = []
        for obj in self.objects:
            tmp_object = {}
            for field in obj._meta.fields:
                tmp_object[field] = getattr(obj, field)
            result.append(tmp_object)
        return result
