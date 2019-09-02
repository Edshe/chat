from datetime import datetime

import peewee as models
from .base import BaseModel


class User(BaseModel):
    """
    Model represents users. Needs to display
    users info in chat rooms.
    """
    id = models.UUIDField(
        unique=True,
        primary_key=True
    )
    email = models.CharField(
        unique=True
    )
    name = models.CharField()


class Room(BaseModel):
    """
    Model represents Rooms.
    """
    @classmethod
    async def all_rooms(cls, objects):
        """ Return all rooms """
        return await objects.execute(cls.select())

    async def all_messages(self, objects):
        """ Return all messages """
        return await objects.prefetch(self.messages, User.select())

    def __str__(self):
        return f'{self.id}'


class Message(BaseModel):

    """ Chat Message model """

    user = models.ForeignKeyField(
        User,
        null=True,
        related_name='messages'
    )
    room = models.ForeignKeyField(
        Room,
        related_name='messages'
    )
    text = models.TextField()

    created_at = models.DateTimeField(
        default=datetime.utcnow()
    )

    class Meta:
        order_by = ('created_at', )

    def __str__(self):
        return f'{self.user.email} - {self.text}'

    def __dict__(self):
        """
        Method return dict repr of message
        """
        return {
            'text': self.text,
            'created_at': self.created_at.isoformat(),
            'user': self.user.username if self.user else None}
