from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import MySerializer
import json

class MyAPIView(APIView):
    """ Clase que recibe un JSON y lo imprime en la consola """
    def post(self, request, *args, **kwargs):
        """ Método que recibe un JSON y lo imprime en la consola """
        print(json.dumps(request.data, indent=4))
        # serializer = MySerializer(data=request.data)
        return Response(request.data, status=status.HTTP_200_OK)
        # if serializer.is_valid():
        #     print(json.dumps(serializer.validated_data, indent=4))  # Imprime el JSON en la consola
        #     return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
