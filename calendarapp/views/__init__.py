""" This module contains all the views for the calendarapp app. """
from .event_list import AllEventsListView, RunningEventsListView
from .other_views import (
    CalendarViewNew,
    CalendarView,
    create_event,
    EventEdit,
    event_details,
    add_eventmember,
    EventMemberDeleteView,
    DashboardView,
)


__all__ = [
    'AllEventsListView',
    'RunningEventsListView',
    'CalendarViewNew',
    'CalendarView',
    'create_event',
    'EventEdit',
    'event_details',
    'add_eventmember',
    'EventMemberDeleteView',
    'DashboardView',
]
