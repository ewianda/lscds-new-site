from django.conf.urls import patterns, url
from event.views import (EventDetailView,email_preview,EventArchiveIndexView,EventTypeListView,EventTypeDetailView)

urlpatterns = patterns('',
    url(r'^email_preview/$', email_preview, name='email_preview'),                   
    url(r'^(?P<slug>[\w-]+)/$', EventTypeDetailView.as_view(), name='event-type-detail'),
    url(r'^$', EventTypeListView.as_view(), name='event-list'),
     url(r'^email_preview/$', email_preview, name='email_preview'),
    
    url(r'^archive/$',
       EventArchiveIndexView.as_view(),
        name="article_archive"),
    url(r'^event-details/(?P<slug>[\w-]+)/$',EventDetailView.as_view(),name="event-detail"),
)



