from django.contrib import admin
from event.models import (Event, Registration, Talk, Presenter,EventType)



class EventlineAdmin(admin.StackedInline):
    model = Event
    extra = 0


class TalklineAdmin(admin.TabularInline):
    model = Talk
    extra = 1


class PresenterlineAdmin(admin.TabularInline):
    model = Presenter
    extra = 1

class RegistrationlineAdmin(admin.TabularInline):
    model = Registration
    extra = 0

class EventTypeAdmin(admin.ModelAdmin):
    inlines = [
       EventlineAdmin
    ]

class EventAdmin(admin.ModelAdmin):
    inlines = [
       RegistrationlineAdmin,TalklineAdmin
    ]
class PresenterAdmin(admin.ModelAdmin):
   pass


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
