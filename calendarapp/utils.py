""" This file contains the Calendar class which is used to render the calendar in the template. """
# calendarapp/utils.py
from calendar import HTMLCalendar
from .models import Event


class Calendar(HTMLCalendar):
    """ Calendar class to render the calendar in the template. """
    def __init__(self, year=None, month=None):
        self.year = year
        self.month = month
        super().__init__()

    # formats a day as a td
    # filter events by day
    def formatday(self, day, weekday):
        """ formats a day as a td """
        events_per_day = weekday.filter(start_time__day=day)
        d = ""
        for event in events_per_day:
            d += f"<li> {event.get_html_url} </li>"
        if day != 0:
            return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
        return "<td></td>"

    # formats a week as a tr

    def formatweek(self, theweek, events):
        """ formats a week as a tr """
        week = ""
        for d, _ in theweek:
            week += self.formatday(d, events)
        return f"<tr> {week} </tr>"

    # formats a month as a table
    # filter events by year and month
    def formatmonth(self, theyear=None, themonth=None, withyear=True):
        """ formats a month as a table """
        if theyear is None:
            theyear = self.year
        if themonth is None:
            themonth = self.month
        events = Event.objects.filter(
            start_time__year=self.year, start_time__month=self.month
        )
        cal = (
            '<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        )  # noqa
        cal += (
            f"{self.formatmonthname(theyear, themonth, withyear=withyear)}\n"
        )  # noqa
        cal += f"{self.formatweekheader()}\n"
        for week in self.monthdays2calendar(theyear, themonth):
            cal += f"{self.formatweek(week, events)}\n"
        return cal
