import settings
from core.base import db
from core.models import Room, User, Message

db.init(**settings.DATABASE)
db.create_tables([Message, Room, User])