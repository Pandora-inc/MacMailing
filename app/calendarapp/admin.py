from django.contrib import admin
from calendarapp import models


@admin.register(models.Event)
class EventAdmin(admin.ModelAdmin):
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

    def get_queryset(self, request):
        """
        Return the queryset of EventMember instances to be displayed in the admin interface.
        
        This method is called by the admin interface to retrieve the queryset of EventMember instances
        that will be displayed in the list view. By default, it returns all instances of the model.
        """
        return super().get_queryset(request)

    def get_list_display(self, request):
        """
        Return the list of fields to be displayed in the list view of the admin interface.
        
        This method is called by the admin interface to determine which fields of the EventMember instances
        should be displayed in the list view. By default, it returns the list_display attribute of the class.
        """
        return super().get_list_display(request)

    def get_list_filter(self, request):
        """
        Return the list of fields to be used as filters in the admin interface.
        
        This method is called by the admin interface to determine which fields of the EventMember instances
        should be used as filters in the list view. By default, it returns the list_filter attribute of the class.
        """
        return super().get_list_filter(request)
