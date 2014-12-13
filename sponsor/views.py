from django.shortcuts import render

# Create your views here.
from django.views.generic.list import ListView
from sponsor.models import Sponsor

class SponsorListView(ListView):
       model = Sponsor




