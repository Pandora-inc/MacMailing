
import os.path
import json
import requests
import json

from reportes.models import Clientes
from reportes.serializers import ClientesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ast import literal_eval

# from .serializers import BitrixIncomingSerializer as MySerializer

class MyAPIView(APIView):
    """ Clase que recibe un JSON y lo imprime en la consola """

    WEB_HOOK = os.getenv("WEB_HOOK")
    def post(self, request, *args, **kwargs):
        """ Método que recibe un JSON y lo imprime en la consola """
        data = request.data
        changed_data_id = data['data[FIELDS][ID]']

        base_url = "https://b24-tgz7td.bitrix24.es/rest/1/b5a32slysrg26vwr/crm.contact.get.json?ID="
        url = base_url + changed_data_id

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = requests.request("POST", url, headers=headers)

        data = json.loads(response.content)
        if data.get('result'):
            data = data.get('result')

        cliente_id = data.get('cliente_id', data.get('ID'))

        if not cliente_id:
            return Response({"error": "cliente_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente = Clientes.objects.get(cliente_id=cliente_id)
        except Clientes.DoesNotExist:
            return Response({"error": "Cliente not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ClientesSerializer(cliente, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
