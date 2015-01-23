# Create your views here.
from django.views.generic import TemplateView
from event.models import EventBanner

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['banners'] = EventBanner.objects.all()[:4]
        return context
    
