""" This module contains the admin interface for the calendarapp models. """
from django.contrib import admin
from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
    """ Admin interface for managing Event instances. """
    model = models.Event
    list_display = [
        "id",
        "title",
        "user",
        "is_active",
        "is_deleted",
        "created_at",
        "updated_at",
    ]
    list_filter = ["is_active", "is_deleted"]
    search_fields = ["title"]


@admin.register(models.EventMember)
class EventMemberAdmin(admin.ModelAdmin):
    """
    Admin interface for managing EventMember instances.

    This class allows the admin to view and edit the details of the EventMember instances,
    which represent the relationship between a user and an event in the calendar app.
    The main functionalities of this class include displaying the list of EventMember instances,
    filtering them by event, and showing their details in the admin interface.
    """

    model = models.EventMember
    list_display = ["id", "event", "user", "created_at", "updated_at"]
    list_filter = ["event"]
