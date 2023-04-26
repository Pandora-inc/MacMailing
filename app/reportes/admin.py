""" Configuraciones del Admin """
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from .models import (Countrys, ContactType, WebType, EmailType, SocialType, Clientes, ClientesContact,
                             ClientesWeb, ClientesEmail, ClientesSocial, ClientesAddress, ClientesUTM, ExcelFiles, Account, MailCorp)



class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'supervisor']
    search_fields = ['name', 'supervisor']
    ordering = ['name', 'supervisor']
    list_filter = ['supervisor']
    # inlines = [CompaniasInline]

class ClientesAdmin(admin.ModelAdmin):
    list_display = ['cliente_id', 'last_name', 'first_name', 'middle_name', 'lead_name', 'status', 'responsible']
    search_fields = ['cliente_id', 'last_name','lead_name', 'status', 'responsible']
    ordering = ['cliente_id', 'last_name','lead_name', 'status', 'responsible']
    list_filter = ['responsible' ,'lead_name']


class ClientesAddressAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'address', 'city', 'postal_code', 'country']
    search_fields = ['cliente', 'address','city', 'postal_code', 'country']
    ordering = ['cliente', 'address','city', 'postal_code', 'country']
    list_filter = ['cliente' ,'address']

class ClientesContactAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type','data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente' ,'type']

class ClientesEmailAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type','data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente' ,'type']

class ClientesSocialAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type','data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente' ,'type']

class ClientesUTMAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'source', 'campaign','content']
    search_fields = ['cliente', 'source','campaign','content']
    ordering = ['cliente', 'campaign']
    list_filter = ['cliente' ,'campaign']

class ClientesWebAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type','data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente' ,'type']

class MailCorpAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'account', 'user']
    search_fields = ['name', 'email', 'account', 'user']
    ordering = ['name', 'email', 'account', 'user']
    list_filter = ['account', 'user']
    
class ExcelFilesAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'create_user']
    search_fields = ['name', 'file', 'create_user']
    ordering = ['name', 'file', 'create_user']
    list_filter = ['create_user']

admin.site.register(Clientes, ClientesAdmin)
admin.site.register(ClientesAddress, ClientesAddressAdmin)
admin.site.register(ClientesContact, ClientesContactAdmin)
admin.site.register(ClientesEmail, ClientesEmailAdmin)
admin.site.register(ClientesSocial, ClientesSocialAdmin)
admin.site.register(ClientesUTM, ClientesUTMAdmin)
admin.site.register(ClientesWeb, ClientesWebAdmin)
admin.site.register(Countrys)
admin.site.register(ContactType)
admin.site.register(WebType)
admin.site.register(EmailType)
admin.site.register(SocialType)
admin.site.register(ExcelFiles, ExcelFilesAdmin)


admin.site.register(Account, AccountAdmin)
admin.site.register(MailCorp, MailCorpAdmin)