from django.contrib import admin
from event.models import (Resource, Registration, Talk, Presenter,ResourceType)



class ResourcelineAdmin(admin.StackedInline):
    model = Resource
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

class ResourceTypeAdmin(admin.ModelAdmin):
    inlines = [
       ResourcelineAdmin
    ]

class ResourceAdmin(admin.ModelAdmin):
    inlines = [
       RegistrationlineAdmin,TalklineAdmin
    ]
class PresenterAdmin(admin.ModelAdmin):
   pass


admin.site.register(ResourceType, ResourceTypeAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Presenter, PresenterAdmin)
