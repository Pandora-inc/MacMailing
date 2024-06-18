""" Configuraciones del Admin """
from django import forms
from django.contrib import admin, messages

from auxiliares.models import EmailType
from reportes.actions import (get_mail_data,
                     get_template_file_and_save,
                     prepare_email_body, send_mail)
from reportes.models import (Clientes, ClientesEmail, ExcelFiles, Mail, MailCorp)
from reportes.utils import UtilExcelFile, get_response_account, if_admin



def procesar_excel(modeladmin, request, queryset):
    ''' Función para procesar los archivos excel '''
    for obj in queryset:
        try:
            file = ExcelFiles.objects.get(id=obj.id)
            excel = UtilExcelFile()
            excel.open_file(file.file.path)

            excel.print_datos()
        except Exception as e:
            mensaje = f"Error in excel, The format must be Excel Workbook (xlsx): {e}"
            messages.error(request, mensaje)


procesar_excel.short_description = "Process Excel"



def template_file_propague(modeladmin, request, queryset):
    ''' Función para propagar las plantillas '''
    for obj in queryset:
        try:
            get_template_file_and_save(obj.id)
        except Exception as e:
            messages.error(request, f"Error propagating: {e}")

template_file_propague.short_description = "Template Propagation"






class AccountAdmin(admin.ModelAdmin):
    ''' Admin View for Account '''
    list_display = ['name', 'supervisor']
    search_fields = ['name', 'supervisor']
    ordering = ['name', 'supervisor']
    list_filter = ['supervisor']

    # DEPRECATED - Se usa get_queryset
    # def get_queryset(self, request):
    #     # Obtener el queryset base
    #     queryset = super().get_queryset(request)

    #     if not if_admin(request.user):
    #         queryset = queryset.filter(supervisor=request.user)

    #     return queryset







class ClientesAddressAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesAddress
    '''
    list_display = ['cliente', 'address', 'city', 'postal_code', 'country']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'address',
                     'city',
                     'postal_code',
                     'country__description']
    ordering = ['cliente', 'address', 'city', 'postal_code', 'country']
    list_filter = ['cliente', 'address']


class ClientesContactAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesContact
    '''
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'type__name',
                     'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']




class ClientesSocialAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesSocial
    '''
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'type__name',
                     'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


class ClientesUTMAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesUTM
    '''
    list_display = ['cliente', 'source', 'campaign', 'content']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'source',
                     'campaign',
                     'content']
    ordering = ['cliente', 'campaign']
    list_filter = ['cliente', 'campaign']


class ClientesWebAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesWeb
    '''
    list_display = ['cliente', 'type', 'data']
    search_fields = ['cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'type__name',
                     'data']
    ordering = ['cliente', 'type']
    list_filter = ['cliente', 'type']


class MailCorpAdmin(admin.ModelAdmin):
    '''
    Admin View for MailCorp
    '''
    list_display = ['name', 'email', 'account', 'user']
    search_fields = ['name', 'email', 'account__name', 'user__username']
    ordering = ['name', 'email', 'account', 'user']
    list_filter = ['account', 'user']

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            queryset = queryset.filter(user=request.user)

        return queryset


class ExcelFilesAdmin(admin.ModelAdmin):
    '''
    Admin View for ExcelFiles
    '''
    list_display = ['name', 'file', 'create_user']
    search_fields = ['name', 'file', 'create_user__username']
    ordering = ['name', 'file', 'create_user']
    list_filter = ['create_user']

    actions = [procesar_excel]


class AttachmentAdmin(admin.ModelAdmin):
    '''
    Admin View for Attachment
    '''
    list_display = ['name', 'file', 'created']
    search_fields = ['name', 'file', 'created']
    ordering = ['name', 'file', 'created']


class TemplateGroupAdmin(admin.ModelAdmin):
    '''
    Admin View for TemplateGroup
    '''
    list_display = ['name', 'mail_corp']
    search_fields = ['name',
                     'mail_corp__name',
                     'mail_corp__email']
    readonly_fields = ('create_user',)
    ordering = ['name', 'mail_corp']

    # DEPRECATED - Se usa get_queryset
    # def get_queryset(self, request):
    #     '''
    #     Filtra los grupos de templates por la cuenta del usuario
    #     '''
    #     queryset = super().get_queryset(request)

    #     if not if_admin(request.user):
    #         accounts = get_response_account(request.user)
    #         queryset = queryset.filter(mail_corp__in=accounts)

    #     return queryset

    def save_model(self, request, obj, form, change):
        if not obj.create_user:
            # Asigna el usuario actual
            obj.create_user = request.user
        super().save_model(request, obj, form, change)


class TemplateFilesAdmin(admin.ModelAdmin):
    '''
    Admin View for TemplateFiles
    '''
    list_display = ['name', 'orden', 'template_group']
    search_fields = ['name', 'orden', 'template_group__name']
    readonly_fields = ('create_user',)
    ordering = ['name', 'orden', 'template_group__name']
    list_filter = ['template_group', 'create_user']

    # DEPRECATED - Se usa get_queryset
    # def get_queryset(self, request):
    #     '''
    #     Filtra los templates por la cuenta del usuario
    #     '''
    #     queryset = super().get_queryset(request)

    #     if not if_admin(request.user):
    #         accounts = get_response_account(request.user)
    #         groups = TemplatesGroup.objects.filter(mail_corp__in=accounts)
    #         queryset = queryset.filter(template_group__in=groups)

    #     return queryset

    def save_model(self, request, obj, form, change):
        if not obj.create_user:
            # Asigna el usuario actual
            obj.create_user = request.user
        super().save_model(request, obj, form, change)

    actions = [template_file_propague]
