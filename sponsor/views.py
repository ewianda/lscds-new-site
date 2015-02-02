from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from sponsor.models import Sponsor,EventSponsor

class SponsorListView(ListView):
       model = Sponsor     
       
       def get_context_data(self, **kwargs):
        context = super(SponsorListView, self).get_context_data(**kwargs)
        context['event_sponsors'] = EventSponsor.objects.all()
        return context




