import asyncio
from peewee import *
from datetime import datetime

db = SqliteDatabase('people.db')

class Person(Model):
    name = CharField()
    birthday = DateField()

    class Meta:
        database = db

db.connect()
db.create_tables([Person, ])


i = 1



def sync_process_user():
    for i in range(1000):
          Person(name='Bob', birthday=datetime.now()).save()
    return True

def sync_create_user():
    global i
    print(f"Creating user {i}")
    sync_process_user()
    print(f"Created user {i}")
    i += 1

async def process_user():
    for i in range(1000):
          Person(name='Bob', birthday=datetime.now()).save()
    return True



async def create_user():
    global i
    print(f"Creating user {i}")

    await  asyncio.wait([process_user()])
    print(f"Created user {i}")
    i += 1


start = datetime.now()
ioloop = asyncio.get_event_loop()
tasks = [ioloop.create_task(create_user()) for i in range(10)]

wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()

# for i in range(10):
#     sync_create_user()
print(datetime.now() - start)