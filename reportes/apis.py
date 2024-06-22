
import os.path
import json
import requests
import json

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
        content = literal_eval(data['_content'])

        changed_data_id = content['data[FIELDS][ID]']

        base_url = "https://b24-tgz7td.bitrix24.es/rest/1/b5a32slysrg26vwr/crm.contact.get.json?ID="
        url = base_url + changed_data_id

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.request("POST", url, headers=headers)
        print(response)
        print(response.text)
        # https://b24-tgz7td.bitrix24.es/rest/1/b5a32slysrg26vwr/crm.contact.get.json?ID=2
        # serializer = MySerializer(data=request.data)
        return Response(response.content, status=status.HTTP_200_OK)
        # if serializer.is_valid():
            # print(json.dumps(serializer.validated_data, indent=4))  # Imprime el JSON en la consola

            # return Response(serializer.data, status=status.HTTP_200_OK)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
