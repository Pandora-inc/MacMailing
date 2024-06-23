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
    cc = serializers.ListField(child=serializers.EmailField(),
                               allow_empty=True,
                               required=False,
                               allow_null=True)
    date = serializers.DateTimeField()
    content = serializers.CharField()
    number = serializers.IntegerField()
    content_type = serializers.CharField()
    from_pass = serializers.CharField()
    from_smtp = serializers.CharField()
    from_port = serializers.IntegerField()
    salutation = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    last_name = serializers.CharField()
    lead_name = serializers.CharField()
    data = serializers.CharField()
    company_name = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    position = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    type = serializers.CharField()
    firma = serializers.CharField(required=False, allow_null=True, allow_blank=True)
    user_name = serializers.CharField()
    user_last_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    mail_id = serializers.IntegerField()
    mail_to_send_id = serializers.IntegerField()
