from django.conf.urls import patterns, url
from event.views import (EventDetailView,EventArchiveIndexView,EventTypeListView,EventTypeDetailView)

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', EventTypeDetailView.as_view(), name='event-type-detail'),
    url(r'^$', EventTypeListView.as_view(), name='event-list'),
    url(r'^archive/$',
       EventArchiveIndexView.as_view(),
        name="article_archive"),
    url(r'^event-details/(?P<slug>[\w-]+)/$',EventDetailView.as_view(),name="event-detail"),
)



