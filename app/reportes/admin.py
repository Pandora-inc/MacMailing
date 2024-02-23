""" Configuraciones del Admin """
from datetime import date
from django.utils.safestring import mark_safe
from django.utils import timezone
from django.contrib import admin, messages

from auxiliares.models import EmailType

from .utils import UtilExcelFile
from .actions import (actualizar_con_template,
                      get_mail_data,
                      get_template_file_and_save,
                      prepare_email_body,
                      send_mail)
from .models import (Attachment,
                     Mail,
                     TemplateFiles,
                     TemplatesGroup,
                     Clientes,
                     ClientesContact,
                     ClientesWeb,
                     ClientesEmail,
                     ClientesSocial,
                     ClientesAddress,
                     ClientesUTM,
                     ExcelFiles,
                     Account,
                     MailCorp,
                     MailsToSend)


def enviar_email(modeladmin, request, queryset):
    """ Función para enviar email desde el admin """
    try:
        for obj in queryset:
            if obj.approved is True:
                if send_mail(obj.mail_id):
                    # TODO esto es lo que hay que agregar para que registre el mail enviado
                    obj.send = True
                    obj.save()
            else:
                messages.warning(request, "Email no aprobado")
                print("Email no aprobado")
    except Exception as e:
         messages.error(request, f"Error al enviar: {e}")

enviar_email.short_description = "Send email"


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


def prepare_to_send(modeladmin, request, queryset):
    ''' Función para preparar los emails para enviar '''
    for obj in queryset:
        if obj.status_response is False:
            mail = MailsToSend()
            mail.mail = obj
            mail.save()

prepare_to_send.short_description = "Prepare shipment"


def template_file_propague(modeladmin, request, queryset):
    ''' Función para propagar las plantillas '''
    for obj in queryset:
        try:
            get_template_file_and_save(obj.id)
        except Exception as e:
            messages.error(request, f"Error propagating: {e}")

template_file_propague.short_description = "Template Propagation"


def if_admin(user):
    """ Función para verificar si el usuario es admin """
    if user.is_superuser:
        return True
    else:
        grupos = user.groups.all()

        for grupo in grupos:
            if grupo.name == 'SuperAdmin' or grupo.name == 'Admin':
                return True

        return False


def get_response_account(user):
    ''' Obtener las cuentas de respuesta del usuario '''
    return MailCorp.objects.filter(user=user)


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


class ClientesEmailInline(admin.TabularInline):
    '''
    Tabular Inline View for ClientesEmail
    '''
    model = ClientesEmail


class ClientesAdmin(admin.ModelAdmin):
    ''' Admin View for Clientes '''
    list_display = ['cliente_id', 'last_name', 'first_name',
                    'middle_name', 'lead_name', 'status', 'responsible', 'contacted']
    search_fields = ['cliente_id', 'last_name',
                     'lead_name', 'status', 'responsible__name', 'contacted']
    ordering = ['cliente_id', 'last_name',
                'lead_name', 'status', 'responsible', 'contacted']
    list_filter = ['contacted', 'responsible', 'lead_name']
    inlines = [ClientesEmailInline]

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            queryset = queryset.filter(responsible__in=accounts)

        return queryset


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


class ClientesEmailAdmin(admin.ModelAdmin):
    '''
    Admin View for ClientesEmail
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

    def get_queryset(self, request):
        ''' Obtener el queryset base '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(cliente__in=clientes)

        return queryset


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


class MailAdmin(admin.ModelAdmin):
    '''
    Admin View for Mail
    '''
    class Media:
        ''' Media files for admin '''
        js = ('admin/js/admin/admin_script.js',)

    list_display = ['mail_corp', 'cliente', 'subject', 'send_number',
                    'status', 'status_response', 'last_send', 'proximo']
    search_fields = ['mail_corp__name',
                     'mail_corp__email',
                     'cliente__lead_name',
                     'cliente__first_name',
                     'cliente__last_name',
                     'cliente__cliente_id',
                     'subject',
                     'send_number', 
                     'status',
                     'last_send']
    ordering = ['mail_corp', 'cliente', 'subject',
                'send_number', 'status', 'last_send']
    list_filter = ['mail_corp', 'send_number', 'status', 'status_response']
    readonly_fields = ('body', 'subject', 'last_send', 'send_number', 'created')

    actions = [prepare_to_send]

    def get_queryset(self, request):
        # Obtener el queryset base
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            # clientes = Clientes.objects.filter(responsible__in=accounts)

            queryset = queryset.filter(mail_corp__in=accounts)

        return queryset

    def get_readonly_fields(self, request, obj=None):
        # Si 'fin' es True, establece los campos como readonly
        if obj and obj.status_response:
            return self.readonly_fields + ('mail_corp', 'cliente', 'subject', 'body',
                                           'attachment', 'status', 'status_response',
                                           'template_group', 'reminder_days', 'use_template',) 
        return self.readonly_fields

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        # Define una función para filtrar los clientes basados en el campo 'responsable'
        if db_field.name == "cliente":
            if not if_admin(request.user):
                accounts = get_response_account(request.user)
                # clientes = Clientes.objects.filter(responsible__in=accounts)
                # Filtra los clientes cuyo 'responsable' coincide con un ID particular
                kwargs["queryset"] = Clientes.objects.filter(responsible__in=accounts)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


    def proximo(self, obj):
        '''
        Calcula los días que faltan para el proximo envío
        '''
        last_send = obj.last_send
        if obj.status_response:
            return " - "

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

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        if obj.use_template and obj.template_group and obj.send_number == 0:
            actualizar_con_template(obj.id)


class MailInline(admin.TabularInline):
    '''
    Tabular Inline View for Mail
    '''
    model = ClientesEmail


class MailsToSendAdmin(admin.ModelAdmin):
    '''
    Admin View for MailsToSend
    '''
    list_display = ['mail', 'approved', 'send', 'mail_to', 'mail_from']
    readonly_fields = (
        'mail_from',
        'mail_subject',
        'mail_body',
        'user_approved',
        'date_approved')
    search_fields = ['mail__mail_corp__name', 'mail__cliente__lead_name', 'approved', 'send']
    ordering = ['mail', 'approved', 'send']

    def get_queryset(self, request):
        '''
        Filtra los mails que se van a enviar
        '''
        queryset = super().get_queryset(request)

        if not if_admin(request.user):
            accounts = get_response_account(request.user)
            mails = Mail.objects.filter(mail_corp__in=accounts)
            queryset = queryset.filter(mail__in=mails, send=False)
        else:
            queryset = queryset.filter(send=False)

        return queryset

    def mail_body(self, obj):
        '''
        Muestra el cuerpo del mail
        '''
        body = obj.mail.body
        body += '<br>'+obj.mail.mail_corp.firma
        msg_data = get_mail_data(obj.mail.id)
        body = prepare_email_body(body, msg_data)

        return mark_safe(body)

    def mail_subject(self, obj):
        '''
        Muestra el asunto del mail
        '''
        return obj.mail.subject

    def mail_from(self, obj):
        '''
        Muestra el mail del remitente
        '''
        return obj.mail.mail_corp.email

    def mail_to(self, obj):
        '''
        Muestra el mail del destinatario
        '''
        # FIXME: Esto debería mostrar el mail principar del cliente
        email = ClientesEmail.objects.get(
            cliente=obj.mail.cliente, type=EmailType.objects.get(id=1))
        return email

    def save_model(self, request, obj, form, change):
        # Verifica si el campo 'approved' cambió a True y 'user_approved' aún no está establecido
        if obj.approved and not obj.user_approved:
            # Asigna el usuario actual
            obj.user_approved = request.user
            # Asigna la fecha y hora actual
            obj.date_approved = timezone.now()
        super().save_model(request, obj, form, change)

    mail_body.short_description = 'Cuerpo del Email'
    mail_subject.short_description = 'Asunto del Email'

    actions = [enviar_email]


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


admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Clientes, ClientesAdmin)
admin.site.register(ClientesAddress, ClientesAddressAdmin)
admin.site.register(ClientesContact, ClientesContactAdmin)
admin.site.register(ClientesEmail, ClientesEmailAdmin)
admin.site.register(ClientesSocial, ClientesSocialAdmin)
admin.site.register(ClientesUTM, ClientesUTMAdmin)
admin.site.register(ClientesWeb, ClientesWebAdmin)
admin.site.register(ExcelFiles, ExcelFilesAdmin)
admin.site.register(Mail, MailAdmin)
admin.site.register(MailsToSend, MailsToSendAdmin)
admin.site.register(Account, AccountAdmin)
admin.site.register(MailCorp, MailCorpAdmin)
admin.site.register(TemplatesGroup, TemplateGroupAdmin)
admin.site.register(TemplateFiles, TemplateFilesAdmin)
