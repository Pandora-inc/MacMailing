from datetime import datetime
from django.test import TestCase
from calendarapp.models import Event
from reportes.actions import crear_evento
from reportes.models import Mail


class MailTestCase(TestCase):
    """ Test Mail model and functions """

    def test_creates_new_event(self):
        """ Test that a new event is created """
        # Arrange
        mail = Mail()
        mail.send_number = 1
        mail.subject = "Test Subject"
        mail.last_send = datetime.now()
        mail.reminder_days = 7

        # Act
        crear_evento(mail)

        # Assert
        assert Event.objects.filter(title="1 - Test Subject").exists()
