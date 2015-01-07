from django.conf.urls import patterns, url
from event.views import EventMonthArchiveView,EventArchiveIndexView,EventTypeListView,EventTypeDetailView

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', EventTypeDetailView.as_view(), name='event-detail'),
    url(r'^$', EventTypeListView.as_view(), name='event-list'),
    url(r'^archive/$',
       EventArchiveIndexView.as_view(),
        name="article_archive"),
    # Example: /2012/aug/
    url(r'^event/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        EventMonthArchiveView.as_view(),
        name="archive_month"),
    # Example: /2012/08/
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$',
        EventMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
)



