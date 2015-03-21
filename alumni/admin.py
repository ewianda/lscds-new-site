from django.contrib import admin
from alumni.models import Alumni,AlumniRegistration
from communication.action import send_EMAIL
send_EMAIL.short_description = 'Send RSVP'
# Register your models here.
class AlumniAdmin(admin.ModelAdmin):
    list_display=('first_name','last_name','email','company','position')
    actions = [send_EMAIL]
                    
                    
                    
#admin.site.register(Alumni, AlumniAdmin)  
#admin.site.register(AlumniRegistration)