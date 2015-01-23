from django.contrib import admin
from event.models import (Event, Registration, Talk, Presenter,EventType,RoundTable,RoundTableRegistration,EventFee,EventBanner)
from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.mail import send_mass_mail

class EmailAdminForm(forms.Form):
    subject = forms.CharField()
    message = forms.CharField(widget=CKEditorWidget())
    

class EventCreationForm(forms.ModelForm):
    model = Event
    def clean(self):
        cleaned_data = super(EventCreationForm, self).clean()
        registration_start = cleaned_data.get("registration_start")
        registration_end = cleaned_data.get("registration_end")
        starts = cleaned_data.get("starts")
       
        if registration_start > registration_end:
             raise forms.ValidationError("Registration must start before it ends. Please check the registration dates")   
              
        elif registration_start > starts:
             raise forms.ValidationError("Registration cannot start after event date. Please check the Event dates")
        else:
             return self.cleaned_data

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
    form = EventCreationForm
    inlines = [
     EventFeelineAdmin, RoundTablelineAdmin,RegistrationlineAdmin,TalklineAdmin
    ]
    
class PresenterAdmin(admin.ModelAdmin):
   pass

class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('owner','event', 'created')
    list_filter = ['event']
    search_fields = ['owner']

class BannerAdmin(admin.ModelAdmin):
    list_display = ('eventtype','position', 'admin_image')
   
    
    
    
class RoundTableAdmin(admin.ModelAdmin):
    inlines = [RoundTableRegistrationlineAdmin
    ]
from smtplib import SMTPException
from lscds_site.utils import send_mass_html_mail

from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
class RoundTableRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student','round_table', 'created','event')
    list_filter = ['round_table','round_table__event']
    search_fields = ['student']
    actions = ['send_EMAIL']
    def send_EMAIL(self, request, queryset):
        cont_html = "email/email.html"
        cont_txt = "email/email.txt"

        context = {
                'title': _("Send Email"),
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,
                
            }
        
        if request.POST.get('post'):
            form = EmailAdminForm(request.POST)          
            if form.is_valid(): 
                messages = ()                 
                subject = form.cleaned_data['subject']
                message = form.cleaned_data['message']
                for q in queryset:
                    content = {"user":q.student.get_full_name(),"message":message}
                    txt=render_to_string(cont_txt,content)
                    html=render_to_string(cont_html,content)
                    compose=(subject,txt,html,"no-reply@lscds.org",[q.student.email])
                    messages =messages + (compose,)                                
            # process the queryset here
                
                try:
                    send_mass_html_mail(messages ,fail_silently=False)                
                    self.message_user(request, "Mail sent successfully ")  
                except SMTPException:                  
                    self.message_user(request, "Mail was no sent please contact admin for assistance")                
            else:
                context.update({"form":form})
                return TemplateResponse(request, 'admin/send_email.html',
                context, current_app=self.admin_site.name)
        else:
            form = EmailAdminForm()
            context.update({"form":form})
            return TemplateResponse(request, 'admin/send_email.html',
                context, current_app=self.admin_site.name)


admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(RoundTable,RoundTableAdmin)
admin.site.register(RoundTableRegistration,RoundTableRegistrationAdmin)
admin.site.register(Registration,RegistrationAdmin)
admin.site.register(EventBanner,BannerAdmin)
