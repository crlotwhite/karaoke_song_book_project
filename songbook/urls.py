from django.urls import path

from .views import (
    test,
    HowtoView,
)
urlpatterns = [
    path('', test, name='test'),
    path('howto/', HowtoView.as_view(), name='howto'),
]
