from django.urls import path

from .views import (
    test,
    SongList,
    HowtoView,
)
urlpatterns = [
    path('', test, name='test'),
    path('howto/', HowtoView.as_view(), name='howto'),
    path('list/', SongList.as_view(), name='songlist'),
]
