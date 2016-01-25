from django.contrib import admin
from event.models import *


from django.contrib.admin import helpers
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from django import forms
from ckeditor.widgets import CKEditorWidget
from django.core.mail import send_mass_mail
from sponsor.models import EventSponsor
from django.forms.models import BaseInlineFormSet
from event.forms import EmailAdminForm
from smtplib import SMTPException
from lscds_site.utils import send_mass_html_mail
from lscds_site.utils  import export_as_csv_action
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.template import Context, Template
from google.appengine.api import mail
from communication.action import send_EMAIL
from django.contrib.admin.models import LogEntry, DELETION
from django.utils.html import escape
from django.core.urlresolvers import reverse
from easy_select2 import select2_modelform
from actions.actions import mark_attendance

class RequiredInlineFormSet(BaseInlineFormSet):
    """
    Generates an inline formset that is required
    """

    def _construct_form(self, i, **kwargs):
        """
        Override the method to change the form attribute empty_permitted
        """
        form = super(RequiredInlineFormSet, self)._construct_form(i, **kwargs)
        form.empty_permitted = False
        return form

class EventCreationForm(forms.ModelForm):
    model = Event
    def clean(self):
        cleaned_data = super(EventCreationForm, self).clean()
        registration_start = cleaned_data.get("registration_start")
        registration_end = cleaned_data.get("registration_end")
        starts = cleaned_data.get("starts")

        if registration_start and registration_end and registration_start > registration_end:
             raise forms.ValidationError("Registration must start before it ends. Please check the registration dates")

        elif registration_start and starts and registration_start > starts:
             raise forms.ValidationError("Registration cannot start after event date. Please check the Event dates")
        else:
             return self.cleaned_data

class EventlineAdmin(admin.StackedInline):
    model = Event
    extra = 0
    
    
class EventSponsorlineAdmin(admin.StackedInline):
    model = EventSponsor
    extra = 0



class TalklineAdmin(admin.TabularInline):
    model = Talk
    extra = 0
class CompanylineAdmin(admin.TabularInline):
    model = EventCompany
    extra = 0   
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
    
class CDPanelistlineAdmin(admin.TabularInline):
    model = CDPanelist
    extra = 6   
    
    
class BaseRequiredInline(admin.TabularInline):
    extra = 1
    max_num = 1
    formset = RequiredInlineFormSet
    
class EventFeelineAdmin(BaseRequiredInline):
    model =EventFee
    


class RegTemplineAdmin(BaseRequiredInline):
    model =EventRegistrationTemplate
 
    
class ModTemplateAdmin(BaseRequiredInline):   
    model =EventModifyTemplate
 
    
class DeleteTemplate(BaseRequiredInline):
    model =EventDeleteTemplate
 
    
class EventTypeAdmin(admin.ModelAdmin):    
    
    inlines = [
       EventlineAdmin
    ]
  
class CDPanelAdmin(admin.ModelAdmin):    
    
    inlines = [CDPanelistlineAdmin
      
    ]  
    
class EventTypeAdmin(admin.ModelAdmin):    
    
    inlines = [
       EventlineAdmin
    ]





class EventAdmin(admin.ModelAdmin):
    form = EventCreationForm
    inlines = [
     RoundTablelineAdmin,TalklineAdmin,CompanylineAdmin,EventSponsorlineAdmin,RegTemplineAdmin,ModTemplateAdmin,DeleteTemplate
    ]
    prepopulated_fields = {"slug": ("name","location")}
    list_display = ('name',)
    
    
class PresenterAdmin(admin.ModelAdmin):
    list_display = ('full_name','email','qualification', 'position','company')    
    list_select_related = ('event',)
    list_filter = ['name']
    send_EMAIL.short_description = 'Send RSVP'
    actions = [send_EMAIL]
#     search_fields = ['name']

RegistrationForm = select2_modelform(Registration, attrs={'width': '250px'})

class RegistrationAdmin(admin.ModelAdmin):
    form =RegistrationForm
    list_display = ('owner','email' ,'event','attended', 'created')
    list_filter = ['event']
    search_fields = ['owner__email','owner__last_name','owner__first_name']
    send_EMAIL.short_description = 'Send Reminder email'
    actions = [mark_attendance,send_EMAIL,export_as_csv_action("Export CVS")]
    
    
    
class BannerAdmin(admin.ModelAdmin):
    list_display = ('eventtype','position', 'admin_image')




class RoundTableAdmin(admin.ModelAdmin):
    inlines = [RoundTableRegistrationlineAdmin
    ]
class CDRegistrationAdmin(admin.ModelAdmin):
     list_display = ('student','cd_pannel', 
                    'session','attended','department','faculty','degree','event','created')
    
     list_filter = ['session','cd_pannel','cd_pannel__event']
     search_fields = ['student__email','student__last_name','student__first_name']
     send_EMAIL.short_description = 'Send Reminder email'
     actions = [mark_attendance,send_EMAIL,export_as_csv_action("Export CVS")]
    
class RoundTableRegistrationAdmin(admin.ModelAdmin):
    list_display = ('student','round_table', 
                    'session','attended','department','faculty','event','created')
    
    list_filter = ['session','round_table','round_table__event']
    search_fields = ['student__email','student__last_name','student__first_name']
    actions = [mark_attendance,'send_EMAIL',export_as_csv_action("Export CVS")]
 
    
    
    def send_EMAIL(self, request, queryset):
        cont_html = "email/email.html"
        cont_txt = "email/email.txt"

        context = {
                'title': _("Send Email"),
                'queryset': queryset,
                'action_checkbox_name': helpers.ACTION_CHECKBOX_NAME,

            }
        email_message = mail.EmailMessage(sender="Life Sciences Career Development Society <contact@lscds.org>")

        if request.POST.get('post'):
            form = EmailAdminForm(request.POST)
            if form.is_valid():
                messages = ()
                from django.contrib.sites.models import Site       
                if Site._meta.installed:
                     site = Site.objects.get_current()
                else:
                     site = RequestSite(request) 
                subject = form.cleaned_data['subject']
                form_message = form.cleaned_data['message']
                event = form.cleaned_data['event']  
                t=Template(form_message) 
                email_message.subject = subject 
                #for i in range(20):    
                for q in queryset:
                    user = q.student
                    rt1,rt2=RoundTable.objects.get_user_rountable(user,event)
                    
                    c =Context({'rt1':rt1[0].guest,'rt2':rt2[0].guest,'event':event})
                    render_message= t.render(c)    
                                  
                    content = {"user":user,"message":render_message,'site':site}                      
                    txt=render_to_string(cont_txt,content)
                    html=render_to_string(cont_html,content)
                    email_message.body=txt
                    email_message.html = html
                    email_message.to = q.student.email
                    email_message.send()
                    
                    compose=(subject,txt,html,"no-reply@lscds.org",[q.student.email])
                    messages =messages + (compose,)
                    
            # process the queryset here

                try:
                    #send_mass_html_mail(messages ,fail_silently=False)
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




class LogEntryAdmin(admin.ModelAdmin):

    date_hierarchy = 'action_time'

    readonly_fields = LogEntry._meta.get_all_field_names()

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    search_fields = [
        'object_repr',
        'change_message'
    ]


    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
        'change_message',
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return request.user.is_superuser and request.method != 'POST'

    def has_delete_permission(self, request, obj=None):
        return False

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = u'<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return link
    object_link.allow_tags = True
    object_link.admin_order_field = 'object_repr'
    object_link.short_description = u'object'
    
    def queryset(self, request):
        return super(LogEntryAdmin, self).queryset(request) \
            .prefetch_related('content_type')
            
            
class AdditionalGuestAdmin(admin.ModelAdmin):
    list_display = ('full_name','email','qualification', 'position','company','event')  
    list_filter = ['attending','name']
    search_fields = ['name','last_name']
    send_EMAIL.short_description = 'Send Reminder email'
    actions = [send_EMAIL,export_as_csv_action("Export CVS")]
    
    
 # This is a general admin for Exec, Alumini and general registration    
class EventRegistrationAdmin(admin.ModelAdmin):   
    send_EMAIL.short_description = 'Send Reminder email'
    actions = [send_EMAIL,export_as_csv_action("Export CVS")]
    list_display = ('event','name','plus_one',) 
    list_filter = ['event',]
    
    
    
admin.site.register(AdditionalGuestRegistration,AdditionalGuestAdmin)
    
          
admin.site.register(LogEntry, LogEntryAdmin)             
admin.site.register(EventType, EventTypeAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Presenter, PresenterAdmin)
admin.site.register(RoundTable,RoundTableAdmin)
admin.site.register(RoundTableRegistration,RoundTableRegistrationAdmin)
admin.site.register(Registration,RegistrationAdmin)
admin.site.register(CDRegistration,CDRegistrationAdmin)
admin.site.register(EventBanner,BannerAdmin)
admin.site.register(EventCompany)
admin.site.register(AlumniRegistration,EventRegistrationAdmin)
admin.site.register(GuestRegistration,EventRegistrationAdmin)
admin.site.register(CDPanels,CDPanelAdmin)
admin.site.register(MembershipFee)



#admin.site.register(EventSchedule)
#admin.site.register(Schedule)


