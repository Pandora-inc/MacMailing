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



class ClientesSerializer(serializers.ModelSerializer):
    """ Serializer para el modelo Clientes """
    class Meta:
        model = Clientes
        fields = '__all__'
        required = False
