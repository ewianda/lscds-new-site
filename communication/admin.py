from django.contrib import admin
from communication.models import LscdsEmail,EmailTemplate,ListServ
from lscdsUser.models import MailingList,OldlscdsUser
from communication.forms import EmailAdminForm

# Register your models here.

def get_list_serv():
    old_users = OldlscdsUser.objects.all().exclude(mailinglist=False)
    mailing_list = MailingList.objects.all()
    users = ListServ.objects.all().exclude(mailinglist=False).exclude(email__icontains = "lscds.org")
    return old_users,mailing_list,users

class ListServAdmin(admin.ModelAdmin):
     def get_queryset(self, request):
        qs = super(ListServAdmin, self).get_queryset(request)           
        return qs.exclude(mailinglist=False).exclude(email__icontains = "lscds.org")
     def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        old_users,mailing_list,users =get_list_serv()
        extra_context['mailing_list']=mailing_list.exclude(newsletter_only =True)
        extra_context['old_users'] = old_users
        extra_context['users'] = users
        extra_context['form'] = EmailAdminForm()
        return super(ListServAdmin, self).changelist_view(request, extra_context=extra_context)

admin.site.register(LscdsEmail)
admin.site.register(EmailTemplate)
admin.site.register(ListServ,ListServAdmin)