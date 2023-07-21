''' Conjunto de modelos auxiliares para la aplicación '''
from django.db import models


class Type(models.Model):
    ''' Typos de compañías '''
    name = models.CharField(max_length=64, blank=True, null=True)
    description = models.CharField(max_length=64, blank=True, null=True)

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
