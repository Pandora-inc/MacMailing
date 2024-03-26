from datetime import datetime
from django.test import TestCase
from django.contrib.auth.models import User

from reportes.actions import crear_evento
# from reportes.models import Mail
from reportes.models import Mail, MailCorp
from calendarapp.models import Event

class MailTestCase(TestCase):
    """ Test Mail model and functions """

    def setUp(self):
        # set up a users
        User.objects.create_user(
            username='test', password='test1234'
        )
        self.client.login(username='test', password='test1234')
        self.test_user = User.objects.get(username='test')

        self.test_mail_corp = MailCorp.objects.create(
            user=self.test_user
        )


    def test_creates_new_event(self):
        """ Test that a new event is created """
        # mock_object = MockObject(1)
        # assert mock_object.get_value() == 1
        # Arrange
        mail = Mail()
        mail.send_number = 1
        mail.subject = "Test Subject"
        mail.last_send = datetime.now()
        mail.reminder_days = 7
        mail.mail_corp = self.test_mail_corp

        # Act
        crear_evento(mail)

        # Assert
        assert Event.objects.filter(title="1 - Test Subject").exists()
