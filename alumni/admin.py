from django.contrib import admin
from alumni.models import AlumniTab                 
class AlumniTabAdmin(admin.ModelAdmin):
      prepopulated_fields = {"slug": ("name",)}                  
admin.site.register(AlumniTab,AlumniTabAdmin)  
#admin.site.register(AlumniRegistration)