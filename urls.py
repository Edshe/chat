from core import views

routes = (
    dict(method='GET', path='/chat/rooms/{slug}', handler=views.RoomView, name='list-room'),
    dict(method='POST', path='/chat/rooms/', handler=views.RoomView, name='create-room'),
    dict(method='GET', path='/ws/{slug}', handler=views.WebSocket, name='ws'),
)
