from django.conf.urls import patterns, url
from sponsor.views import SponsorListView


urlpatterns = patterns('',
    url(r'^$', SponsorListView.as_view(), name='sponsor-list'),
    
    )
