from django.urls import path

from .views import (
    test,
    SongList,
)
urlpatterns = [
    path('', test, name='test'),
    path('list/', SongList.as_view(), name='songlist'),
]
