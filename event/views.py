from django.shortcuts import render
from django.views.generic.dates import MonthArchiveView,ArchiveIndexView
from event.models import Event,EventType
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.utils import timezone

class EventTypeDetailView(DetailView):
    model = EventType

    def get_context_data(self, **kwargs):
        context = super(EventTypeDetailView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventTypeListView(ListView):
    #paginate_by=1
    model = EventType

    def get_context_data(self, **kwargs):
        context = super(EventTypeListView, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context

class EventArchiveIndexView(ArchiveIndexView):
     model = Event
     date_field = "starts"
     paginate_by=3



class EventMonthArchiveView(MonthArchiveView):
    queryset = Event.objects.all()
    date_field = "starts"
    make_object_list = True
    allow_future = True
    paginate_by=3
    template_name='event/event_archive.html', 
