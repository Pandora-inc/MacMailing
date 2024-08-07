""" This file contains the views for the calendarapp app. """

import calendar

from datetime import timedelta, datetime, date

from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.views import generic
from django.utils.safestring import mark_safe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse

from reportes.utils import if_admin
from calendarapp.models import EventMember, Event
from calendarapp.utils import Calendar
from calendarapp.forms import EventForm, AddMemberForm


def get_date(req_day):
    """ Get the date from the request. """
    if req_day:
        year, month = (int(x) for x in req_day.split("-"))
        return date(year, month, day=1)
    return datetime.today()


def prev_month(d):
    """ Get the previous month URL. """
    first = d.replace(day=1)
    prev_month_date = first - timedelta(days=1)
    return f"month={prev_month_date.year}-{prev_month_date.month}"

def next_month(d):
    """ Get the next month URL. """
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    next_month_date = d + timedelta(days=days_in_month)
    return f"month={next_month_date.year}-{next_month_date.month}"


class CalendarView(LoginRequiredMixin, generic.ListView):
    """ Calendar view """
    model = Event
    template_name = "calendar.html"

    def get_context_data(self, **kwargs):
        """ Get the context data. """
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get("month", None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context["calendar"] = mark_safe(html_cal)
        context["prev_month"] = prev_month(d)
        context["next_month"] = next_month(d)
        return context


# @login_required(login_url="signup")
def create_event(request):
    """ Create event """
    form = EventForm(request.POST or None)
    if request.POST and form.is_valid():
        title = form.cleaned_data["title"]
        description = form.cleaned_data["description"]
        start_time = form.cleaned_data["start_time"]
        end_time = form.cleaned_data["end_time"]
        Event.objects.get_or_create(
            user=request.user,
            title=title,
            description=description,
            start_time=start_time,
            end_time=end_time,
        )
        return HttpResponseRedirect(reverse("calendarapp:calendar"))
    return render(request, "event.html", {"form": form})


class EventEdit(generic.UpdateView):
    """ Edit event """
    model = Event
    fields = ["title", "description", "start_time", "end_time"]
    template_name = "event.html"


# @login_required(login_url="signup")
def event_details(request, event_id):
    """ Event details """
    event = Event.objects.get(id=event_id)
    eventmember = EventMember.objects.filter(event=event)
    context = {"event": event, "eventmember": eventmember}
    return render(request, "event-details.html", context)


def add_eventmember(request, event_id):
    """ Add event member """
    forms = AddMemberForm()
    if request.method == "POST":
        forms = AddMemberForm(request.POST)
        if forms.is_valid():
            member = EventMember.objects.filter(event=event_id)
            event = Event.objects.get(id=event_id)
            if member.count() <= 9:
                user = forms.cleaned_data["user"]
                EventMember.objects.create(event=event, user=user)
                return redirect("calendarapp:calendar")
            print("--------------User limit exceed!-----------------")
    context = {"form": forms}
    return render(request, "add_member.html", context)


class EventMemberDeleteView(generic.DeleteView):
    """ Delete event member """
    model = EventMember
    template_name = "event_delete.html"
    success_url = reverse_lazy("calendarapp:calendar")


class CalendarViewIndex(LoginRequiredMixin, generic.base.TemplateView):
    """ Calendar view """
    # login_url = "accounts:signin"
    template_name = "templates/admin/index/admin_index.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        """ Get method for the calendar view. """
        forms = self.form_class()

        if if_admin(request.user):
            events = Event.objects.get_all()
            events_month = Event.objects.get_all_running_events()
        else:
            events = Event.objects.get_all_events(user=request.user)
            events_month = Event.objects.get_running_events(user=request.user)


        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),

                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)


class CalendarViewNew(LoginRequiredMixin, generic.View):
    """ Calendar view """
    # login_url = "accounts:signin"
    template_name = "calendarapp/calendar.html"
    form_class = EventForm

    def get(self, request, *args, **kwargs):
        """ Get method for the calendar view. """
        forms = self.form_class()

        if if_admin(request.user):
            events = Event.objects.get_all()
            events_month = Event.objects.get_all_running_events()
        else:
            events = Event.objects.get_all_events(user=request.user)
            events_month = Event.objects.get_running_events(user=request.user)


        event_list = []
        # start: '2020-09-16T16:00:00'
        for event in events:
            event_list.append(
                {
                    "title": event.title,
                    "start": event.start_time.strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": event.end_time.strftime("%Y-%m-%dT%H:%M:%S"),
                }
            )
        context = {"form": forms, "events": event_list,
                   "events_month": events_month}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        """ Post method for the calendar view. """
        forms = self.form_class(request.POST)
        if forms.is_valid():
            form = forms.save(commit=False)
            form.user = request.user
            form.save()
            return redirect("calendarapp:calendar")
        context = {"form": forms}
        return render(request, self.template_name, context)



class DashboardView(LoginRequiredMixin, generic.View):
    """ Dashboard view """
    login_url = "accounts:signin"
    template_name = "calendarapp/dashboard.html"

    def get(self, request, *args, **kwargs):
        """ Get method for the dashboard view. """
        if if_admin(request.user):
            events = Event.objects.get_all()
        else:
            events = Event.objects.get_all_events(user=request.user)

        running_events = Event.objects.get_running_events(user=request.user)
        latest_events = Event.objects.filter(user=request.user).order_by("-id")[:10]
        context = {
            "total_event": events.count(),
            "running_events": running_events,
            "latest_events": latest_events,
        }
        return render(request, self.template_name, context)
