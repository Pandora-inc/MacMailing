""" Configuraciones del Admin """
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from reportes.models import (Countrys,ContactType,WebType,EmailType,SocialType,Clientes,ClientesContact,ClientesWeb,ClientesEmail,ClientesSocial,ClientesAddress,ClientesUTM)



admin.site.register(Countrys)
admin.site.register(ContactType)
admin.site.register(WebType)
admin.site.register(EmailType)
admin.site.register(SocialType)
admin.site.register(Clientes)
admin.site.register(ClientesContact)
admin.site.register(ClientesWeb)
admin.site.register(ClientesEmail)
admin.site.register(ClientesSocial)
admin.site.register(ClientesAddress)
admin.site.register(ClientesUTM)
