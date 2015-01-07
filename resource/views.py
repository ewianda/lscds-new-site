from django.shortcuts import render
from django.views.generic.dates import MonthArchiveView,ArchiveIndexView
from event.models import Resource,ResourceType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

class ResourceTypeDetailView(DetailView):
    model = ResourceType

    def get_context_data(self, **kwargs):
        context = super(ResourceTypeDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ResourceTypeListView(ListView):
    #paginate_by=1
    model = ResourceType

    def get_context_data(self, **kwargs):
        context = super(ResourceTypeListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class ResourceArchiveIndexView(ArchiveIndexView):
     model = Resource
     date_field = "date_posted"
     paginate_by=3



class ResourceMonthArchiveView(MonthArchiveView):
    queryset = Resource.objects.all()
    date_field = "starts"
    make_object_list = True
    allow_future = True
    paginate_by=3
    template_name='resource/resource_archive.html', 
