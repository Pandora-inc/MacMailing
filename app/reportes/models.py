""" Modelo de datos relacionados a la actividad """
from django.db import models
from django.contrib.auth.models import User
from auxiliares.models import ContactType, Country, EmailType, SocialType, WebType, Type
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver


SALUDATIONS = [('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.'),
               ('Dr.', 'Dr.'), ('Prof.', 'Prof.'), ('Other', 'Other')]
CURRENCYS = [('US Dollar', 'US Dollar'),]


class Account(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    supervisor = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class MailCorp(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    # password = models.CharField(_('password'), max_length=64, blank=True, null=True)
    password = models.CharField(max_length=64, blank=True, null=True)
    smtp = models.CharField(max_length=64, blank=True, null=True)
    smtp_port = models.CharField(max_length=64, blank=True, null=True)
    imap = models.CharField(max_length=64, blank=True, null=True)
    imap_port = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.RESTRICT, blank=True, null=True)
    user = models.ForeignKey(User, models.RESTRICT)
    firma = RichTextUploadingField(
        blank=True, null=True)  # CKEditor Rich Text Field

    def __str__(self):
        return str(self.name)


class Clientes(models.Model):
    """ Modelo para el registro de los clientes """
    cliente_id = models.IntegerField(blank=True, null=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    lead_name = models.CharField(max_length=64, blank=True, null=True)
    salutation = models.CharField(
        max_length=16, blank=True, null=True, choices=SALUDATIONS)
    first_name = models.CharField(max_length=32, blank=True, null=True)
    middle_name = models.CharField(max_length=32, blank=True, null=True)
    last_name = models.CharField(max_length=32, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created = models.DateTimeField(blank=True, null=True)
    source = models.CharField(max_length=32, blank=True, null=True)
    responsible = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True, related_name='responsable')
    status_information = models.CharField(max_length=32, blank=True, null=True)
    source_information = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True, related_name='creado_por')
    modified = models.DateTimeField(blank=True, null=True)
    modified_by = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True, related_name='modificado_por')
    company_name = models.CharField(max_length=64, blank=True, null=True)
    position = models.CharField(max_length=64, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    total = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    currency = models.CharField(
        max_length=16, blank=True, null=True, choices=CURRENCYS)
    product = models.CharField(max_length=32, blank=True, null=True)
    price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    created_by_crm_form = models.CharField(
        max_length=32, blank=True, null=True)
    repeat_lead = models.BooleanField(blank=True, null=True, default=False)
    client = models.CharField(max_length=32, blank=True, null=True)
    customer_journey = models.CharField(max_length=32, blank=True, null=True)
    type = models.ForeignKey(Type, models.RESTRICT, blank=True, null=True)
    country = models.ForeignKey(
        Country, models.RESTRICT, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.RESTRICT, blank=True, null=True)
    addl_type_details_other = models.CharField(
        max_length=32, blank=True, null=True)
    industry_sub_type = models.CharField(max_length=32, blank=True, null=True)
    last_updated_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.cliente_id) + " - " + str(self.first_name) + " " + str(self.last_name) + " - " + str(self.lead_name)

    def add_contact(self, type, data):
        contact = ClientesContact(cliente=self, type=type, data=data)
        contact.save()

    def add_web(self, type, data):
        web = ClientesWeb(cliente=self, type=type, data=data)
        web.save()

    def add_address(self, type, data):
        address = ClientesAddress(cliente=self, type=type, data=data)
        address.save()

    def add_email(self, type, data):
        email = ClientesEmail(cliente=self, type=type, data=data)
        email.save()

    def add_social(self, type, data):
        social = ClientesSocial(cliente=self, type=type, data=data)
        social.save()

    class Meta:
        """ Meta data del modelo """
        # managed = False
        db_table = 'clientes'
        verbose_name = 'cliente'
        verbose_name_plural = 'clientes'
        ordering = ('cliente_id',)


class ClientesContact(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    type = models.ForeignKey(
        ContactType, models.RESTRICT, blank=True, null=True)
    data = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.data)


class ClientesWeb(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    type = models.ForeignKey(WebType, models.RESTRICT, blank=True, null=True)
    data = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.data)


class ClientesEmail(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    type = models.ForeignKey(EmailType, models.RESTRICT, blank=True, null=True)
    data = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.data)


class ClientesSocial(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    type = models.ForeignKey(
        SocialType, models.RESTRICT, blank=True, null=True)
    data = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self):
        return str(self.data)


class ClientesAddress(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    address = models.CharField(max_length=128, blank=True, null=True)
    street_house_no = models.TextField(blank=True, null=True)
    apartment_office_room_floor = models.CharField(
        max_length=128, blank=True, null=True)
    city = models.CharField(max_length=32, blank=True, null=True)
    district = models.CharField(max_length=32, blank=True, null=True)
    region_area = models.CharField(max_length=32, blank=True, null=True)
    postal_code = models.CharField(max_length=32, blank=True, null=True)
    country = models.ForeignKey(
        Country, models.RESTRICT, blank=True, null=True)


class ClientesUTM(models.Model):
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    source = models.CharField(max_length=64, help_text='Codigo')
    medium = models.CharField(max_length=64, help_text='Medio')
    campaign = models.CharField(max_length=64, help_text='Campaign')
    content = models.CharField(max_length=64, help_text='Content')
    term = models.CharField(max_length=64, help_text='Term')


class Attachment(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TemplatesGroup(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    mail_corp = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TemplateFiles(models.Model):
    name = models.CharField(max_length=64, default="Sudject")
    orden = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='template_files/', blank=True, null=True)
    text = RichTextUploadingField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    template_group = models.ForeignKey(
        TemplatesGroup, models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Mail(models.Model):
    mail_corp = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True)
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    subject = models.CharField(max_length=64, blank=True, null=True)
    body = RichTextUploadingField(
        blank=True, null=True)  # CKEditor Rich Text Field
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    attachment = models.ManyToManyField(Attachment, blank=True)
    status = models.BooleanField(default=False)
    status_response = models.BooleanField(default=False)
    use_template = models.BooleanField(default=False)
    template_group = models.ForeignKey(
        TemplatesGroup, models.RESTRICT, blank=True, null=True)
    send_number = models.IntegerField(default=0)
    last_send = models.DateTimeField(blank=True, null=True)
    reminder_days = models.IntegerField(default=7)

    def __str__(self):
        return str(self.subject)


class MailsToSend (models.Model):
    mail = models.ForeignKey(Mail, models.RESTRICT, blank=True, null=True)
    send = models.BooleanField(default=False)
    user_approved = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)


class UserAcount(models.Model):
    user = models.ForeignKey(User, models.RESTRICT, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.RESTRICT, blank=True, null=True)
    name_usr_acount = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_usr_acount(self):
        return str(self.name_usr_acount)+" ("+str(self.account)+")"


class ExcelFiles(models.Model):
    """
    A Django model that represents an Excel file uploaded by a user.

    Fields:
    - name: The name of the file.
    - file: The actual Excel file.
    - created: The date and time the file was created.
    - create_user: The user who created the file.
    """

    name = models.CharField(max_length=64, blank=True, null=True)
    file = models.FileField(upload_to='excel_files/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)

    def __str__(self):
        """
        Returns the name of the file as a string.
        """
        return str(self.name)


""" 
Lo siguiente se ejecuta al guardar las plantillas. 
"""

def propague_template(id_template: int):
    template = TemplateFiles.objects.get(id=id_template)
    orden = template.orden-1
    mails = Mail.objects.filter(
        template_group_id=template.template_group_id, send_number=orden)

    for mail in mails:
        texto = template.text
        mail.subject = template.name
        mail.body = texto
        mail.save()

@receiver(post_save, sender=TemplateFiles)
def mi_funcion_al_guardar(sender, instance, **kwargs):
    propague_template(instance.id)

post_save.connect(mi_funcion_al_guardar, sender=TemplateFiles)
