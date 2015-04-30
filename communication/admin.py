from django.contrib import admin
from communication.models import LscdsEmail,EmailTemplate,ListServ
# Register your models here.


class ListServAdmin(admin.ModelAdmin):
      pass 

admin.site.register(LscdsEmail)
admin.site.register(EmailTemplate)
admin.site.register(ListServ,ListServAdmin)