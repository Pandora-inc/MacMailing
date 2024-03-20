""" Modelo de datos relacionados a la actividad """
from django.db import models
from django.contrib.auth.models import User
from auxiliares.models import ContactType, Country, EmailType, SocialType, WebType, Type
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_save
from django.dispatch import receiver

SALUTATIONS = [('Mrs.', 'Mrs.'), ('Mr.', 'Mr.'), ('Ms.', 'Ms.'),
               ('Dr.', 'Dr.'), ('Prof.', 'Prof.'), ('Other', 'Other')]
CURRENCY = [('US Dollar', 'US Dollar'),]


class Account(models.Model):
    """
    Account class represents an account in the system.

    Attributes:
        name (str): The name of the account.
        supervisor (User): The supervisor of the account.
        created (datetime): The date and time when the account was created.

    Methods:
        __str__(): Returns a string representation of the account.

    """
    name = models.CharField(max_length=64, blank=True, null=True)
    supervisor = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class MailCorp(models.Model):
    """
    MailCorp class represents a mail corporation in the system.

    Attributes:
        name (str): The name of the mail corporation.
        email (str): The email address of the mail corporation.
        password (str): The password of the mail corporation.
        smtp (str): The SMTP server of the mail corporation.
        smtp_port (str): The SMTP port of the mail corporation.
        imap (str): The IMAP server of the mail corporation.
        imap_port (str): The IMAP port of the mail corporation.
        created (datetime): The date and time when the mail corporation was created.
        account (Account): The account associated with the mail corporation.
        user (User): The user associated with the mail corporation.
        firma (str): The signature of the mail corporation.

    Methods:
        __str__(): Returns a string representation of the mail corporation.

    """
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
    firma = RichTextUploadingField(blank=True, null=True, config_name='awesome_ckeditor')

    def __str__(self):
        return str(self.name)


class Clientes(models.Model):
    """ Modelo para el registro de los clientes """
    cliente_id = models.IntegerField(unique=True)
    status = models.CharField(max_length=32, blank=True, null=True)
    lead_name = models.CharField(max_length=64, blank=True, null=True)
    salutation = models.CharField(
        max_length=16, blank=True, null=True, choices=SALUTATIONS)
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
    position = models.CharField(max_length=256, blank=True, null=True)
    comment = models.TextField(blank=True, null=True)
    total = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    currency = models.CharField(
        max_length=16, blank=True, null=True, choices=CURRENCY)
    product = models.CharField(max_length=32, blank=True, null=True)
    price = models.DecimalField(
        max_digits=11, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    created_by_crm_form = models.CharField(
        max_length=32, blank=True, null=True)
    repeat_lead = models.BooleanField(blank=True, null=True, default=False)
    client = models.CharField(max_length=32, blank=True, null=True)
    customer_journey = models.CharField(max_length=32, blank=True, null=True)
    type = models.ForeignKey(Type, models.RESTRICT)
    country = models.ForeignKey(
        Country, models.RESTRICT, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.RESTRICT, blank=True, null=True)
    addl_type_details_other = models.CharField(
        max_length=32, blank=True, null=True)
    industry_sub_type = models.CharField(max_length=32, blank=True, null=True)
    last_updated_on = models.DateTimeField(blank=True, null=True)
    contacted = models.BooleanField(blank=True, null=True, default=False)
    contacted_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.lead_name) + " - " + str(self.first_name) + " " + str(self.last_name) + " - " + str(self.cliente_id)

    def add_contact(self, type, data):
        """ Agrega un contacto al cliente """
        contact = ClientesContact(cliente=self, type=type, data=data)
        contact.save()

    def add_web(self, type, data):
        """ Agrega un contacto web al cliente """
        web = ClientesWeb(cliente=self, type=type, data=data)
        web.save()

    def add_address(self, type, data):
        """ Agrega una dirección al cliente """
        address = ClientesAddress(cliente=self, type=type, data=data)
        address.save()

    def add_email(self, type, data):
        """ Agrega un email al cliente """
        email = ClientesEmail(cliente=self, type=type, data=data)
        email.save()

    def add_social(self, type, data):
        """ Agrega un contacto social al cliente """
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
    """
    The 'ClientesContact' class represents a contact associated with a client.

    Attributes:
        cliente (ForeignKey): The client associated with the contact.
        type (ForeignKey): The type of contact.
        data (CharField): The contact data or information.

    Methods:
        __str__(): Returns a string representation of the contact.

    """
    cliente = models.ForeignKey(Clientes, models.RESTRICT)
    type = models.ForeignKey(ContactType, models.RESTRICT)
    data = models.CharField(max_length=64)

    class Meta:
        """ Meta data of the model """
        unique_together = ('cliente', 'type')

    def __str__(self):
        return str(self.data)


class ClientesWeb(models.Model):
    """
    The 'ClientesWeb' class represents a web contact associated with a client.

    Attributes:
        cliente (ForeignKey): The client associated with the web contact.
        type (ForeignKey): The type of web contact.
        data (TextField): The data or information related to the web contact.

    Methods:
        __str__(): Returns a string representation of the web contact.

    """
    cliente = models.ForeignKey(Clientes, models.RESTRICT)
    type = models.ForeignKey(WebType, models.RESTRICT)
    data = models.TextField()

    class Meta:
        """ Meta data of the model """
        unique_together = ('cliente', 'type')

    def __str__(self):
        return str(self.data)


class ClientesEmail(models.Model):
    """
    The 'ClientesEmail' class represents an email contact associated with a client.

    Attributes:
        cliente (ForeignKey): The client associated with the email contact.
        type (ForeignKey): The type of email.
        data (CharField): The email address.

    Methods:
        __str__(): Returns a string representation of the email contact.

    """
    cliente = models.ForeignKey(Clientes, models.RESTRICT)
    type = models.ForeignKey(EmailType, models.RESTRICT)
    data = models.CharField(max_length=250)

    class Meta:
        """ Meta data of the model """
        unique_together = ('cliente', 'type')

    def __str__(self):
        return str(self.data)


class ClientesSocial(models.Model):
    """
    The 'ClientesSocial' class represents a social media contact associated with a client.

    Attributes:
        cliente (ForeignKey): The client associated with the social media contact.
        type (ForeignKey): The type of social media.
        data (TextField): The data or information related to the social media contact.

    Methods:
        __str__(): Returns a string representation of the social media contact.

    """
    cliente = models.ForeignKey(Clientes, models.RESTRICT)
    type = models.ForeignKey(SocialType, models.RESTRICT)
    data = models.TextField()

    class Meta:
        """ Meta data of the model """
        unique_together = ('cliente', 'type')
        
    def __str__(self):
        return str(self.data)


class ClientesAddress(models.Model):
    """
    The 'ClientesAddress' class represents an address associated with a client.

    Attributes:
        cliente (ForeignKey): The client associated with the address.
        address (TextField): The full address.
        street_house_no (TextField): The street and house number.
        apartment_office_room_floor (CharField): The apartment, office, room, or floor number.
        city (CharField): The city of the address.
        district (CharField): The district of the address.
        region_area (CharField): The region or area of the address.
        postal_code (CharField): The postal code of the address.
        country (ForeignKey): The country of the address.

    """
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
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
    """
    The 'ClientesUTM' class represents a model for tracking UTM parameters related to a client.

    Attributes:
        cliente (ForeignKey): A foreign key to the 'Clientes' model representing the client.
        source (CharField): A string field representing the UTM source code.
        medium (CharField): A string field representing the UTM medium.
        campaign (CharField): A string field representing the UTM campaign.
        content (CharField): A string field representing the UTM content.
        term (CharField): A string field representing the UTM term.

    """
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    source = models.CharField(max_length=64, help_text='Codigo')
    medium = models.CharField(max_length=64, help_text='Medio')
    campaign = models.CharField(max_length=64, help_text='Campaign')
    content = models.CharField(max_length=64, help_text='Content')
    term = models.CharField(max_length=64, help_text='Term')


class Attachment(models.Model):
    """
    A class representing an attachment.

    Attributes:
        name (str): The name of the attachment.
        file (FileField): The file associated with the attachment.
        created (DateTimeField): The date and time when the attachment was created.

    Methods:
        __str__(): Returns a string representation of the attachment.
    """
    name = models.CharField(max_length=64, blank=True, null=True)
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TemplatesGroup(models.Model):
    """
    TemplatesGroup class represents a group of templates in the system.

    Attributes:
        name (str): The name of the templates group.
        created (datetime): The date and time when the templates group was created.
        create_user (User): The user who created the templates group.
        mail_corp (MailCorp): The mail corporation associated with the templates group.

    Methods:
        __str__(): Returns a string representation of the templates group.

    """
    name = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    mail_corp = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class TemplateFiles(models.Model):
    """
    TemplateFiles class represents a template file in the system.

    Attributes:
        name (str): The name of the template file.
        orden (int): The order number of the template file.
        file (FileField): The file associated with the template file.
        text (RichTextUploadingField): The text content of the template file.
        created (datetime): The date and time when the template file was created.
        create_user (User): The user who created the template file.
        template_group (TemplatesGroup): The templates group associated with the template file.

    Methods:
        __str__(): Returns a string representation of the template file.

    """
    name = models.CharField(max_length=64, default="Sudject", verbose_name="Subject")
    orden = models.PositiveIntegerField(default=1)
    file = models.FileField(upload_to='template_files/', blank=True, null=True)
    text = RichTextUploadingField(blank=True, null=True, config_name='awesome_ckeditor')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    create_user = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    template_group = models.ForeignKey(
        TemplatesGroup, models.RESTRICT, blank=True, null=True)

    def __str__(self):
        return str(self.name)


class Mail(models.Model):
    """
    The 'Mail' class represents an email in the system.

    Attributes:
        mail_corp (ForeignKey): The mail corporation associated with the email.
        cliente (ForeignKey): The client associated with the email.
        subject (str): The subject of the email.
        body (RichTextUploadingField): The body or content of the email.
        created (DateTimeField): The date and time when the email was created.
        attachment (ManyToManyField): The attachments associated with the email.
        status (bool): The status of the email.
        status_response (bool): The status of the email response.
        use_template (bool): Indicates whether the email uses a template.
        template_group (ForeignKey): The templates group associated with the email.
        send_number (int): The number of times the email has been sent.
        last_send (DateTimeField): The date and time of the last email send.
        reminder_days (int): The number of days for email reminder.

    Methods:
        __str__(): Returns a string representation of the email.

    Meta:
        unique_together (tuple): Specifies that the combination of 'cliente' and 
        'mail_corp' should be unique.

    """
    mail_corp = models.ForeignKey(
        MailCorp, models.RESTRICT, blank=True, null=True)
    cliente = models.ForeignKey(
        Clientes, models.RESTRICT, blank=True, null=True)
    subject = models.CharField(max_length=256, blank=True, null=True)
    body = RichTextUploadingField(blank=True, null=True, config_name='awesome_ckeditor')
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

    class Meta:
        """ Meta data of the model """
        unique_together = ('cliente', 'mail_corp')


class MailsToSend (models.Model):
    """
    MailsToSend class represents a model for storing mails to be sent in the system.

    Attributes:
        mail (Mail): The mail object associated with the mail to be sent.
        send (bool): Indicates whether the mail has been sent or not.
        user_approved (User): The user who approved the mail to be sent.
        date_approved (datetime): The date and time when the mail was approved to be sent.
        approved (bool): Indicates whether the mail has been approved to be sent or not.

    Methods:
        __str__(): Returns a string representation of the MailsToSend object.

    """
    mail = models.ForeignKey(Mail, models.RESTRICT, blank=True, null=True)
    send = models.BooleanField(default=False)
    user_approved = models.ForeignKey(
        User, models.RESTRICT, blank=True, null=True)
    date_approved = models.DateTimeField(blank=True, null=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return str(self.mail)


class UserAcount(models.Model):
    """
    UserAcount class represents a user account in the system.

    Attributes:
        user (User): The user associated with the account.
        account (Account): The account associated with the user.
        name_usr_acount (str): The name of the user account.
        created (datetime): The date and time when the user account was created.

    Methods:
        __str__(): Returns a string representation of the user account.
        get_usr_acount(): Returns the name of the user account and the associated account.

    """
    user = models.ForeignKey(User, models.RESTRICT, blank=True, null=True)
    account = models.ForeignKey(
        Account, models.RESTRICT, blank=True, null=True)
    name_usr_acount = models.CharField(max_length=64, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def get_usr_acount(self):
        """ Returns the name of the user account and the associated account. """
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
    """
    Propagates a template to mails with a specific order number.

    Parameters:
        id_template (int): The ID of the template to propagate.

    Returns:
        None

    Raises:
        TemplateFiles.DoesNotExist: If the template with the given ID does not exist.

    Example:
        propague_template(1)

    This function retrieves a template with the given ID and propagates it to mails that
    have a specific order number. It updates the subject and body of each mail with the 
    template's name and text, respectively.
    """
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
    """ Función que se ejecuta al guardar un template """
    propague_template(instance.id)

post_save.connect(mi_funcion_al_guardar, sender=TemplateFiles)
