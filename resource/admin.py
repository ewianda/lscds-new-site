from django.contrib import admin
from resource.models import (Resource, Jobs ,Files) 





class JobAdmin(admin.ModelAdmin):
      pass

class ResourceAdmin(admin.ModelAdmin):
       pass
class FilesAdmin(admin.ModelAdmin):
       pass


admin.site.register(Jobs, JobAdmin)
admin.site.register(Resource, ResourceAdmin)
admin.site.register(Files, FilesAdmin)
