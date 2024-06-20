''' Conjunto de modelos auxiliares para la aplicación '''
from django.db import models


class Type(models.Model):
    ''' Typos de compañías '''
    name = models.CharField(max_length=64, unique=True)
    description = models.CharField(max_length=64, blank=True, null=True)
    code = models.IntegerField(default=0, unique=True)

    def __str__(self):
        return str(self.name)


class Country(models.Model):
    ''' Paises '''
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.description)


class ContactType(models.Model):
    ''' Tipos de contacto '''
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class WebType(models.Model):
    ''' Tipos de web '''
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class EmailType(models.Model):
    ''' Tipos de email '''
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class SocialType(models.Model):
    ''' Tipos de redes sociales '''
    name = models.CharField(max_length=32, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.name)

class Currency(models.Model):
    ''' Tipos de monedas '''
    code = models.CharField(max_length=3)
    amount_cnt = models.IntegerField(blank=True, null=True)
    amount = models.FloatField(blank=True, null=True)
    sort = models.IntegerField(blank=True, null=True)
    base = models.BooleanField(default=False)
    full_name = models.CharField(max_length=32)
    lid = models.CharField(max_length=5)
    format_string = models.CharField(max_length=32)
    dec_point = models.CharField(max_length=1)
    thousands_sep = models.CharField(max_length=1)
    decimals = models.IntegerField(blank=True, null=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)
