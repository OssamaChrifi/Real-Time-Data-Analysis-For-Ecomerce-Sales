from django.urls import path

from .consumers import ChartsConsumer

ws_urlpatterns = [
    path(r'ws/charts/$', ChartsConsumer.as_asgi())
]