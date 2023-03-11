from django.urls import path

from app.views import home, room_create, room

urlpatterns = [
    path('', home, name='home'),
    path('room/create', room_create, name='room-create'),
    path('room/<uuid:pk>', room, name='room'),
]
