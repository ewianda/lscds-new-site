from django.contrib import admin
from event.models import (Event, Registration, Talk, Presenter,EventType,RoundTable,RoundTableRegistration)



class EventlineAdmin(admin.StackedInline):
    model = Event
    extra = 0


class TalklineAdmin(admin.TabularInline):
    model = Talk
    extra = 1
class RoundTableRegistrationlineAdmin(admin.TabularInline):
     model = RoundTableRegistration
     extra = 1

class PresenterlineAdmin(admin.TabularInline):
    model = Presenter
    extra = 1
class RegistrationlineAdmin(admin.TabularInline):
    model = Registration
    extra = 2

class RoundTablelineAdmin(admin.TabularInline):
    model = RoundTable
    extra = 0

class EventTypeAdmin(admin.ModelAdmin):
    inlines = [
       EventlineAdmin
    ]

class EventAdmin(admin.ModelAdmin):
    inlines = [
       RegistrationlineAdmin,TalklineAdmin,RoundTablelineAdmin
    ]
class PresenterAdmin(admin.ModelAdmin):
   pass

class RegistrationAdmin(admin.ModelAdmin):
   pass


class RoundTableAdmin(admin.ModelAdmin):
    inlines = [RoundTableRegistrationlineAdmin
    ]





admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(RoundTable,RoundTableAdmin)
admin.site.register(Registration,RegistrationAdmin)

