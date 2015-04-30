from resource.models import (Resource, Jobs ,Files) 
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone



class ResourceDetailView(DetailView):
      model = Resource
 
class ResourceListView(ListView):
      model = Resource     
      paginate_by = 5
      
      
class JobListView(ListView):
       model = Jobs 
       paginate_by = 5
       
       
class JobDetailView(DetailView):
       model = Jobs 
       
class FileListView(ListView):
       model = Files
       paginate_by = 10
    

