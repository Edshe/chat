import asyncio
from typing import Iterable

from core.base import BaseModel


class JSONModelSerializer:

    def __init__(self, objects):
        if isinstance(objects, Iterable):
            self.objects = objects
        else:
            self.objects = [objects, ]

    async def to_json(self):
        results = []
        for obj in self.objects:
            tmp_object = {}
            for field in obj._meta.fields:
                value = getattr(obj, field)
                try:
                    tmp_object[field] = str(value)
                except:
                    tmp_object[field] = value

            results.append(tmp_object)
        return dict(
            count=len(results),
            results=results
        )

