from auxiliares.models import Country, Type
from reportes.models import Clientes, ClientesAddress, ClientesContact, ClientesEmail
from reportes.serializers import ClientesSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction, IntegrityError

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

        if response.status_code != 200:
            logger.info(response.status_code)
            logger.info(response.json())
            return Response(response.json(), status=response.status_code)

        logger.info(response.json())

        result = response.json().get('result')

        salutation = ''
        if result['HONORIFIC']:
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
            'created': result['DATE_CREATE'],
            'source': source,
            'source_information': result['SOURCE_DESCRIPTION'],
            'modified': result['DATE_MODIFY'],
            'company_name': result['COMPANY_TITLE'],
            'position': result['POST'],
            'comment': result['COMMENTS'],
            'total': result['OPPORTUNITY'],
            'currency': 'US Dollar' if result['CURRENCY_ID'] == 'USD' else result['CURRENCY_ID'],
            'type': lead_type,
            # 'repeat_lead': result['ID'],
            'addl_type_details_other': result['UF_CRM_1660655104670'],
            # 'date_of_birth': result['BIRTHDATE'] if result['BIRTHDATE'] else None,
            # 'created_by': result['ID'],
            # 'modified_by': result['ID'],
            # 'responsible': result['ID'],
            # 'status_information': result['ID'],
            # 'product': result['ID'],
            # 'price': result['ID'],
            # 'quantity': result['ID'],
            # 'created_by_crm_form': result['ID'],
            # 'repeat_lead': result['ID'],
            # 'client': result['ID'],
            # 'customer_journey': result['ID'],
            # 'country': result['ID'],
            # 'account': result['ID'],
            # 'addl_type_details_other': result['ID'],
            # 'industry_sub_type': result['ID'],
            # 'last_updated_on': result['ID'],
            # 'contacted': result['ID'],
            # 'contacted_on': result['ID'],
        }


        try:
            cliente = Clientes.objects.get(cliente_id=result['ID'])
            serializer = ClientesSerializer(cliente, data=data, partial=True)  # partial=True permite actualizaciones parciales
            if serializer.is_valid():
                serializer.save()

                if 'EMAIL' in result:
                    for email in result['EMAIL']:
                        if email['VALUE_TYPE'] == 'WORK':
                            email_type = 1
                        elif email['VALUE_TYPE'] == 'HOME':
                            email_type = 2
                        elif email['VALUE_TYPE'] == 'NEWSLETTER':
                            email_type = 3
                        else:
                            email_type = 4

                        try:
                            with transaction.atomic():
                                ClientesEmail.objects.update_or_create(
                                    cliente=cliente,
                                    type_id=email_type,
                                    defaults={'data': email['VALUE']}
                                )
                        except IntegrityError:
                            # Handle the case where there is a duplicate entry
                            print(f"Duplicate entry found for cliente {cliente} and type_id {email_type}.")

                if 'PHONE' in result:
                    for phone in result['PHONE']:
                        if phone['VALUE_TYPE'] == 'WORK':
                            phone_type = 1
                        elif phone['VALUE_TYPE'] == 'HOME':
                            phone_type = 2
                        elif phone['VALUE_TYPE'] == 'NEWSLETTER':
                            phone_type = 3
                        else:
                            phone_type = 4

                        try:
                            with transaction.atomic():
                                ClientesContact.objects.update_or_create(
                                    cliente=cliente,
                                    data=phone['VALUE'],
                                    type_id=phone_type)
                        except IntegrityError:
                            # Handle the case where there is a duplicate entry
                            print(f"Duplicate entry found for cliente {cliente} and type_id {phone_type}.")

                if result['ADDRESS']:
                    ClientesAddress.objects.update_or_create(
                        cliente=cliente,
                        address=result['ADDRESS'],
                        street_house_no=result['ADDRESS_2'],
                        city=result['ADDRESS_CITY'],
                        postal_code=result['ADDRESS_POSTAL_CODE'],
                        region_area=result['ADDRESS_REGION'],
                        district=result['ADDRESS_PROVINCE'],
                        country=Country.objects.get(description=result['ADDRESS_COUNTRY'])
                    )

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
