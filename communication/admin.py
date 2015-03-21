from django.contrib import admin
from communication.models import LscdsEmail,EmailTemplate
# Register your models here.
admin.site.register(LscdsEmail)
admin.site.register(EmailTemplate)