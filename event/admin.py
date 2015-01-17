from django.contrib import admin
from event.models import (Event, Registration, Talk, Presenter,EventType,RoundTable,RoundTableRegistration,EventFee)



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
class EventFeelineAdmin(admin.TabularInline):
    model =EventFee
    extra = 1
    
    
class EventTypeAdmin(admin.ModelAdmin):
    inlines = [
       EventlineAdmin
    ]

class EventAdmin(admin.ModelAdmin):
    inlines = [
     EventFeelineAdmin, RoundTablelineAdmin,RegistrationlineAdmin,TalklineAdmin
    ]
    
class PresenterAdmin(admin.ModelAdmin):
   pass

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('owner','event', 'created')
    list_filter = ['event']
    search_fields = ['owner']


class RoundTableAdmin(admin.ModelAdmin):
    inlines = [RoundTableRegistrationlineAdmin
    ]

class RoundTableRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student','round_table', 'created','event')
    list_filter = ['round_table','round_table__event']
    search_fields = ['student']



admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(RoundTable,RoundTableAdmin)
admin.site.register(RoundTableRegistration,RoundTableRegistrationAdmin)
admin.site.register(Registration,RegistrationAdmin)

