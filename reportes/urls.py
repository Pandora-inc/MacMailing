from django.urls import path
from .apis import MyAPIView

urlpatterns = [
    path('api/my-endpoint/', MyAPIView.as_view(), name='my-api'),
]
