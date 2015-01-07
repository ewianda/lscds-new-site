from django.conf.urls import patterns, url
from event.views import ResourceMonthArchiveView,ResourceArchiveIndexView,ResourceTypeListView,ResourceTypeDetailView

urlpatterns = patterns('',
    url(r'^(?P<slug>[\w-]+)/$', ResourceTypeDetailView.as_view(), name='event-detail'),
    url(r'^$', ResourceTypeListView.as_view(), name='event-list'),
    url(r'^archive/$',
       ResourceArchiveIndexView.as_view(),
        name="article_archive"),
    # Example: /2012/aug/
    url(r'^event/(?P<year>\d{4})/(?P<month>[-\w]+)/$',
        ResourceMonthArchiveView.as_view(),
        name="archive_month"),
    # Example: /2012/08/
    url(r'^archive/(?P<year>\d{4})/(?P<month>\d+)/$',
        ResourceMonthArchiveView.as_view(month_format='%m'),
        name="archive_month_numeric"),
)


abhiprtuv
