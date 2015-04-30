from django.shortcuts import render
from django.views.generic.list import ListView
from testimonial.models import Testimonial
# Create your views here.

class TestimonialListView(ListView):
    model = Testimonial
    paginate_by = 10
