from rest_framework import serializers
from .models import Clientes, ExcelFiles


class ClientesSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo Clientes """
    class Meta:
        model = Clientes
        fields = '__all__'


class ExcelSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo ExcelFiles """
    class Meta:
        model = ExcelFiles
        fields = '__all__'


# class CompleteExcelSerializer(serializers.ModelSerializer):
#      """ Serializer para el modelo ExcelFiles con los clientes asociados """

#     class Meta:
#         """ Clase Meta """
#         model = ExcelFiles
#         fields = '__all__'

#     def to_representation(self, instance):
#         response = super().to_representation(instance)
#         response['clientes'] = ClientesSerializer(instance.clientes.all(), many=True).data
#         return response

class MailSerializer(serializers.Serializer):
    """ Serializer para el envío de correos electrónicos """

    subject = serializers.CharField(max_length=100)
    from_name = serializers.CharField(max_length=100)
    from_email = serializers.EmailField()
    to = serializers.EmailField()
    cc = serializers.ListField(child=serializers.EmailField())
    date = serializers.DateTimeField()
    content = serializers.CharField()
    number = serializers.IntegerField()
    content_type = serializers.CharField()
    from_pass = serializers.CharField()
    from_smtp = serializers.CharField()
    from_port = serializers.IntegerField()
    salutation = serializers.CharField()
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    lead_name = serializers.CharField()
    data = serializers.CharField()
    company_name = serializers.CharField()
    position = serializers.CharField()
    type = serializers.CharField()
    firma = serializers.CharField()


class BitrixIncomingSerializer(serializers.Serializer):
    """ Serializer para la recepción de correos electrónicos de Bitrix24

    "event": "ONCRMCONTACTUPDATE",
    "event_id": "2",
    "data[FIELDS][ID]": "2",
    "ts": "1718849644",
    "auth[domain]": "b24-tgz7td.bitrix24.es",
    "auth[client_endpoint]": "https://b24-tgz7td.bitrix24.es/rest/",
    "auth[server_endpoint]": "https://oauth.bitrix.info/rest/",
    "auth[member_id]": "4bbd6c4cac68c1b2679b8845c1f63312",
    "auth[application_token]": "peml4jfd0ls52rlgykdtsjjzr58p8a04"

    """
    event = serializers.CharField()
    event_id = serializers.CharField()
    # data_field_id = serializers.CharField()
    data = serializers.DictField()
    # data['FIELDS']['ID'] = serializers.CharField()
    ts = serializers.CharField()
    # auth = serializers.DictField()
