""" Event model """
from datetime import datetime
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model

from calendarapp.models import EventAbstract

User = get_user_model()

class EventManager(models.Manager):
    """ Event manager """

    def get_all(self):
        """ Get all events """
        events = Event.objects.filter(is_active=True, is_deleted=False)
        return events

    def get_all_events(self, user):
        """ Get all events for a user """
        events = Event.objects.filter(user=user, is_active=True, is_deleted=False)
        return events

    def get_all_running_events(self):
        """ Get all running events """
        running_events = Event.objects.filter(
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events

    def get_running_events(self, user):
        """ Get running events for a user """
        running_events = Event.objects.filter(
            user=user,
            is_active=True,
            is_deleted=False,
            end_time__gte=datetime.now().date(),
        ).order_by("start_time")
        return running_events


class Event(EventAbstract):
    """ Event model """

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    title = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    objects = EventManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        """ Get absolute url """
        return reverse("calendarapp:event-detail", args=(self.id,))

    @property
    def get_html_url(self):
        """ Get HTML url """
        url = reverse("calendarapp:event-detail", args=(self.id,))
        return f'<a href="{url}"> {self.title} </a>'
