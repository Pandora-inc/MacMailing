""" Configuraciones del Admin """
from django import forms
from django.utils.html import format_html
from django.contrib import admin
from .actions import send_mail
from .models import (Attachment, Countrys, ContactType, Mail, TemplateFiles, TemplatesGroup, WebType, EmailType, SocialType, Clientes, ClientesContact,
                     ClientesWeb, ClientesEmail, ClientesSocial, ClientesAddress, ClientesUTM, ExcelFiles, Account, MailCorp)

def enviar_email(modeladmin, request, queryset):
    """ Funcion para enviar email desde el admin """
    for obj in queryset:
        send_mail(obj.id)

enviar_email.short_description = "Enviar email"


class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'supervisor']
    search_fields = ['name', 'supervisor']
    ordering = ['name', 'supervisor']
    list_filter = ['supervisor']
    # inlines = [CompaniasInline]


class ClientesAdmin(admin.ModelAdmin):
    list_display = ['cliente_id', 'last_name', 'first_name',
                    'middle_name', 'lead_name', 'status', 'responsible']
    search_fields = ['cliente_id', 'last_name',
                     'lead_name', 'status', 'responsible']
    ordering = ['cliente_id', 'last_name',
                'lead_name', 'status', 'responsible']
    list_filter = ['responsible', 'lead_name']


class ClientesAddressAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'address', 'city', 'postal_code', 'country']
    search_fields = ['cliente', 'address', 'city', 'postal_code', 'country']
    ordering = ['cliente', 'address', 'city', 'postal_code', 'country']
    list_filter = ['cliente', 'address']


class ClientesContactAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type', 'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


class ClientesEmailAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type', 'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


class ClientesSocialAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type', 'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


class ClientesUTMAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'source', 'campaign', 'content']
    search_fields = ['cliente', 'source', 'campaign', 'content']
    ordering = ['cliente', 'campaign']
    list_filter = ['cliente', 'campaign']


class ClientesWebAdmin(admin.ModelAdmin):
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente', 'type', 'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


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


class MailAdmin(admin.ModelAdmin):
    list_display = ['mail_corp', 'cliente', 'subject', 'send_number', 'status', 'status_response', 'last_send']
    search_fields = ['mail_corp', 'cliente', 'subject', 'send_number', 'status', 'last_send']
    ordering = ['mail_corp', 'cliente', 'subject', 'send_number', 'status', 'last_send']
    list_filter = ['mail_corp', 'send_number', 'status']

    actions = [enviar_email]



class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'created']
    search_fields = ['name', 'file', 'created']
    ordering = ['name', 'file', 'created']

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
admin.site.register(Mail, MailAdmin)
admin.site.register(Attachment, AttachmentAdmin)


admin.site.register(Account, AccountAdmin)
admin.site.register(MailCorp, MailCorpAdmin)


admin.site.register(TemplatesGroup)
admin.site.register(TemplateFiles)
