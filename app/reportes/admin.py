""" Configuraciones del Admin """
from datetime import date, datetime
import time
from django import forms
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from django.contrib import admin

from .utils import excelFile
from .actions import get_template_file_and_save, send_mail
from .models import (Attachment, Countrys, ContactType, Mail, TemplateFiles, TemplatesGroup, WebType, EmailType, SocialType, Clientes, ClientesContact,
                     ClientesWeb, ClientesEmail, ClientesSocial, ClientesAddress, ClientesUTM, ExcelFiles, Account, MailCorp, MailsToSend)


def enviar_email(modeladmin, request, queryset):
    """ Funcion para enviar email desde el admin """
    for obj in queryset:
        if obj.approved == True:
            if send_mail(obj.mail_id):
                obj.send = True
                obj.save()
            else:
                print("Error al enviar email")
        else:
            print("Email no aprobado")


enviar_email.short_description = "Enviar email"


def procesar_excel(modeladmin, request, queryset):
    for obj in queryset:
        file = ExcelFiles.objects.get(id=obj.id)
        excel = excelFile()
        excel.open_file(file.file.path)
        excel.print_datos()


procesar_excel.short_description = "Procesar Excel"


def prepare_to_send(modeladmin, request, queryset):
    for obj in queryset:
        mail = MailsToSend()
        mail.mail = obj
        mail.save()

prepare_to_send.short_description = "Preparar envio"


def template_file_propague(modeladmin, request, queryset):
    for obj in queryset:
        get_template_file_and_save(obj.id)
        
template_file_propague.short_description = "Propagacion de plantilla"

def if_admin(user):
    """ Funcion para verificar si el usuario es admin """
    if user.is_superuser:
        return True
    else:
        grupos = user.groups.all()

        for grupo in grupos:
            if grupo.name == 'SuperAdmin' or grupo.name == 'Admin':
                return True

        return False

def get_response_account(user):
    return MailCorp.objects.filter(user=user)


class AccountAdmin(admin.ModelAdmin):
    list_display = ['name', 'supervisor']
    search_fields = ['name', 'supervisor']
    ordering = ['name', 'supervisor']
    list_filter = ['supervisor']
    # inlines = [CompaniasInline]

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            queryset = queryset.filter(supervisor=request.user)

        return queryset


class ClientesAdmin(admin.ModelAdmin):
    list_display = ['cliente_id', 'last_name', 'first_name',
                    'middle_name', 'lead_name', 'status', 'responsible']
    search_fields = ['cliente_id', 'last_name',
                     'lead_name', 'status', 'responsible']
    ordering = ['cliente_id', 'last_name',
                'lead_name', 'status', 'responsible']
    list_filter = ['responsible', 'lead_name']

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            queryset = queryset.filter(responsible__in=accounts)

        return queryset


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

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(cliente__in=clientes)

        return queryset


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

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            queryset = queryset.filter(user=request.user)

        return queryset


class ExcelFilesAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'create_user']
    search_fields = ['name', 'file', 'create_user']
    ordering = ['name', 'file', 'create_user']
    list_filter = ['create_user']

    actions = [procesar_excel]


class MailAdmin(admin.ModelAdmin):
    class Media:
        js = ('admin/js/admin/admin_script.js',)

    list_display = ['mail_corp', 'cliente', 'subject', 'send_number',
                    'status', 'status_response', 'last_send', 'proximo']
    search_fields = ['mail_corp', 'cliente', 'subject',
                     'send_number', 'status', 'last_send']
    ordering = ['mail_corp', 'cliente', 'subject',
                'send_number', 'status', 'last_send']
    list_filter = ['mail_corp', 'send_number', 'status']

    actions = [prepare_to_send]

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            # clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(mail_corp__in=accounts)

        return queryset
    
    def proximo(self, obj):

        last_send = obj.last_send
        if last_send:
            today = date.today()
            pass_days = (today - last_send.date()).days

            reminder = int(obj.reminder_days)

            dias = reminder - pass_days
            if dias >= 0:
                return dias
            else:
                return "Estamos atrasados"
        else:
            return "Today is a great day"


class MailInline(admin.TabularInline):
    model = ClientesEmail

class MailsToSendAdmin(admin.ModelAdmin):

    list_display = ['mail', 'approved', 'send', 'mail_to', 'mail_from']
    readonly_fields = ('mail_from','mail_subject', 'mail_body')
    search_fields = ['mail', 'approved', 'send']
    ordering = ['mail', 'approved', 'send']

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            mails = Mail.objects.filter(mail_corp__in=accounts)
            queryset = queryset.filter(mail__in=mails)

        return queryset
    
    def mail_body(self, obj):
        return mark_safe(obj.mail.body)

    def mail_subject(self, obj):
        return obj.mail.subject

    def mail_from(self, obj):
        return obj.mail.mail_corp.email

    def mail_to(self, obj):
        # FIXME: Esto deberia mostrar el mail principar del cliente
        return obj.mail.mail_corp.email

    mail_body.short_description = 'Cuerpo del Email'
    mail_subject.short_description = 'Asunto del Email'

    actions = [enviar_email]


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'file', 'created']
    search_fields = ['name', 'file', 'created']
    ordering = ['name', 'file', 'created']

class TemplateGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'mail_corp']
    search_fields = ['name', 'mail_corp']
    ordering = ['name', 'mail_corp']
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            queryset = queryset.filter(mail_corp__in=accounts)

        return queryset
    
class TemplateFilesAdmin(admin.ModelAdmin):
    list_display = ['name', 'orden', 'template_group']
    search_fields = ['name', 'orden', 'template_group']
    ordering = ['name', 'orden', 'template_group']

    def get_queryset(self, request):
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            goups = TemplatesGroup.objects.filter(mail_corp__in=accounts)
            queryset = queryset.filter(template_group__in=goups)

        return queryset

    actions = [template_file_propague]

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
admin.site.register(MailsToSend, MailsToSendAdmin)


admin.site.register(Account, AccountAdmin)
admin.site.register(MailCorp, MailCorpAdmin)


admin.site.register(TemplatesGroup,TemplateGroupAdmin)
admin.site.register(TemplateFiles,TemplateFilesAdmin)
