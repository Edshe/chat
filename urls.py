from core import views

routes = (
    dict(method='GET', path='/chat/rooms/{slug}', handler=views.RoomView, name='room'),
    dict(method='GET', path='/ws/{slug}', handler=views.WebSocket, name='ws'),
)
