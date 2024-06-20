from auxiliares.models import Type
from reportes.models import Clientes
from reportes.serializers import ClientesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
# from .serializers import MySerializer
import requests
import json
import logging
import os.path

# Configurar el logging
logging.basicConfig(
    filename='reportes/logs/api.log',  # Nombre del archivo de log
    level=logging.INFO,  # Nivel de logging
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'  # Formato del log
)

logger = logging.getLogger(__name__)

class MyAPIView(APIView):
    """ Clase que recibe un JSON y lo imprime en la consola """

    def get(self, request, *args, **kwargs):
        """ Método que imprime un mensaje en la consola """
        message = "Hola mundo"
        logger.info(message)
        return Response({"message": message}, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        """ Método que recibe un JSON y lo imprime en la consola """
        data = json.dumps(request.data, indent=4)
        logger.info(f"Received data: {data}")
        id = request.data['data[FIELDS][ID]']
        url = f'https://maquiavelo.bitrix24.com/rest/636/{os.environ.get("BITRIX_WEBHOOK", "v0uehhaf88vle9ua")}/crm.lead.get.json?ID={id}'
        logger.info(url)
        headers = {'Content-Type': 'html/text', 'Accept': 'application/json', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        response = requests.post(url, headers=headers)
        logger.info(response.json())

        result = response.json().get('result')

        salutation = ''
        if result['HONORIFIC'] == 'HNR_EN_1': salutation = 'Mr.'
        elif result['HONORIFIC'] == 'HNR_EN_2.': salutation = 'Ms.'
        elif result['HONORIFIC'] == 'HNR_EN_3': salutation = 'Mrs.'
        elif result['HONORIFIC'] == 'HNR_EN_4': salutation = 'Dr.'

        lead_status = ''
        if result['STATUS_ID'] == 'NEW': lead_status = '5% Lead Find'
        elif result['STATUS_ID'] == 'IN_PROCESS': lead_status = '20% Lead Contacted'
        elif result['STATUS_ID'] == 'PROCESSED': lead_status = '35% Lead Responded'
        elif result['STATUS_ID'] == 'UC_Z2R285': lead_status = '50% Meeting / Samples / Prices'
        elif result['STATUS_ID'] == 'UC_2KL9D9': lead_status = '75% Proposal Revision Feedback'
        elif result['STATUS_ID'] == 'UC_R0MHEU': lead_status = '90% Proposal Accepted'
        elif result['STATUS_ID'] == 'CONVERTED': lead_status = '100% Client'
        elif result['STATUS_ID'] == 'JUNK': lead_status = 'On-Ice'
        elif result['STATUS_ID'] == 'UC_CMOTYC': lead_status = 'Do not contact'

        source = ''
        if result['SOURCE_ID'] == 'WEBFORM': source = 'CRM form'
        elif result['SOURCE_ID'] == 'CALLBACK': source = 'Callback'
        elif result['SOURCE_ID'] == 'RC_GENERATOR': source = 'Sales boost'
        elif result['SOURCE_ID'] == 'STORE': source = 'Online Store'
        elif result['SOURCE_ID'] == 'CALL': source = 'Call'

        lead_type = Type.objects.get(code=result['UF_CRM_1644500575']).id

        data = {
            'cliente_id': result['ID'],
            'status': lead_status,
            'lead_name': result['TITLE'],
            'salutation': salutation,
            'first_name': result['NAME'],
            'middle_name': result['SECOND_NAME'],
            'last_name': result['LAST_NAME'],
            # 'date_of_birth': result['BIRTHDATE'] if result['BIRTHDATE'] else None,
            'created': result['DATE_CREATE'],
            'source': source,
            # 'responsible': result['ID'],
            # 'status_information': result['ID'],
            'source_information': result['SOURCE_DESCRIPTION'],
            # 'created_by': result['ID'],
            'modified': result['DATE_MODIFY'],
            # 'modified_by': result['ID'],
            'company_name': result['COMPANY_TITLE'],
            'position': result['POST'],
            'comment': result['COMMENTS'],
            'total': result['OPPORTUNITY'],
            'currency': 'US Dollar' if result['CURRENCY_ID'] == 'USD' else result['CURRENCY_ID'],
            # 'product': result['ID'],
            # 'price': result['ID'],
            # 'quantity': result['ID'],
            # 'created_by_crm_form': result['ID'],
            # 'repeat_lead': result['ID'],
            # 'client': result['ID'],
            # 'customer_journey': result['ID'],
            'type': lead_type,
            # 'country': result['ID'],
            # 'account': result['ID'],
            # 'addl_type_details_other': result['ID'],
            # 'industry_sub_type': result['ID'],
            # 'last_updated_on': result['ID'],
            # 'contacted': result['ID'],
            # 'contacted_on': result['ID'],
        }
        if 'EMAIL' in result:
            logger.info(result['EMAIL'])
        if 'PHONE' in result:
            logger.info(result['PHONE'])

        try:
            cliente = Clientes.objects.get(cliente_id=result['ID'])
            serializer = ClientesSerializer(cliente, data=data, partial=True)  # partial=True permite actualizaciones parciales
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                logger.info(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Clientes.DoesNotExist:
            serializer = ClientesSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                logger.info(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def convert_to_client(data):
    """ Método que convierte un JSON a un objeto de tipo Clientes """
    cliente = ClientesSerializer(data=data)
    if cliente.is_valid():
        return cliente.save()
