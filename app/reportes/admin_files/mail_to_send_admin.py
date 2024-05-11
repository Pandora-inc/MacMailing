

from django.contrib import admin, messages
from django.utils.safestring import mark_safe
from django.utils import timezone

from auxiliares.models import EmailType
from reportes.models import ClientesEmail, Mail
from reportes.utils import if_admin, get_response_account
from reportes.actions import get_mail_data, prepare_email_body, send_mail


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

class MailsToSendAdmin(admin.ModelAdmin):
    '''
    Admin View for MailsToSend
    '''
    list_display = ['mail', 'approved', 'mail_to', 'mail_from']
    exclude = ('send',)
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

        body = obj.mail.body if obj.mail.body else ''
        firma = obj.mail.mail_corp.firma if obj.mail.mail_corp.firma else ''
        body += '<br>' + firma
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

    mail_body.short_description = 'Email Body'
    mail_subject.short_description = 'Email subject'

    actions = [enviar_email]
