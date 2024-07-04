""" Serializers para los modelos de la aplicación reportes """
from rest_framework import serializers
from .models import Clientes, ExcelFiles, Mail


class ExcelSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo ExcelFiles """
    class Meta:
        model = ExcelFiles
        fields = '__all__'


class MailSerializer(serializers.Serializer):
    """ Serializer para el envío de correos electrónicos """

    subject = serializers.CharField(max_length=100)
    from_name = serializers.CharField(max_length=100)
    from_email = serializers.EmailField()
    to = serializers.EmailField()
    cc = serializers.ListField(child=serializers.EmailField(), allow_empty=True,
                               required=False, allow_null=True)
    date = serializers.DateTimeField()
    content = serializers.CharField()
    number = serializers.IntegerField()
    content_type = serializers.CharField()
    from_pass = serializers.CharField()
    from_smtp = serializers.CharField()
    from_port = serializers.IntegerField()
    salutation = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    first_name = serializers.CharField()
    middle_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    last_name = serializers.CharField()
    lead_name = serializers.CharField()
    data = serializers.CharField()
    company_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    position = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    type = serializers.CharField()
    firma = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    user_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    user_last_name = serializers.CharField(allow_blank=True, required=False, allow_null=True)
    mail_id = serializers.IntegerField()
    mail_to_send_id = serializers.IntegerField(required=False, allow_null=True)

    def create(self, validated_data):
        """ Crear un objeto Mail """
        return Mail(**validated_data)

    def update(self, instance, validated_data):
        """ Actualizar un objeto Mail """
        instance.subject = validated_data.get('subject', instance.subject)
        instance.from_name = validated_data.get('from_name', instance.from_name)
        instance.from_email = validated_data.get('from_email', instance.from_email)
        instance.to = validated_data.get('to', instance.to)
        instance.cc = validated_data.get('cc', instance.cc)
        instance.date = validated_data.get('date', instance.date)
        instance.content = validated_data.get('content', instance.content)
        instance.number = validated_data.get('number', instance.number)
        instance.content_type = validated_data.get('content_type', instance.content_type)
        instance.from_pass = validated_data.get('from_pass', instance.from_pass)
        instance.from_smtp = validated_data.get('from_smtp', instance.from_smtp)
        instance.from_port = validated_data.get('from_port', instance.from_port)
        instance.salutation = validated_data.get('salutation', instance.salutation)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.middle_name = validated_data.get('middle_name', instance.middle_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.lead_name = validated_data.get('lead_name', instance.lead_name)
        instance.data = validated_data.get('data', instance.data)
        instance.company_name = validated_data.get('company_name', instance.company_name)
        instance.position = validated_data.get('position', instance.position)
        instance.type = validated_data.get('type', instance.type)
        instance.firma = validated_data.get('firma', instance.firma)
        return instance

class ClientesSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo Clientes """
    class Meta:
        model = Clientes
        fields = '__all__'
        required = False
