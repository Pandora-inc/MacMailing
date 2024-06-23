from django.urls import path

from reportes.views import UpdateClientesView
from .apis import MyAPIView

urlpatterns = [
    path('api/update_clientes/', UpdateClientesView.as_view(), name='update_clientes'),
    path('api/my-endpoint/', MyAPIView.as_view(), name='my-api'),
]
