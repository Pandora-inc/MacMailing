""" URLs for the reportes app. """
from django.urls import path
from .apis import MyAPIView

urlpatterns = [
    path('api/update_client/',
         MyAPIView.as_view(http_method_names=['post']),
         name='update-client'),
    path('api/delete_client/',
         MyAPIView.as_view(http_method_names=['delete']),
         name='delete-client'),
]
