from django.conf.urls import patterns, url
from resource.views import ResourceDetailView,JobListView,JobDetailView,FileListView,ResourceListView

urlpatterns = patterns('',
   url(r'^resource-useful-links/$',ResourceListView.as_view(), name='resources-list'),          
   url(r'^our-resources/(?P<slug>[\w-]+)/$', ResourceDetailView.as_view(), name='resources'),
   url(r'^our-job/(?P<slug>[\w-]+)/$',  JobDetailView.as_view(), name='job'),
   url(r'^our-job-postings/$',  JobListView.as_view(), name='job-list'),
   url(r'^uploads/$',  FileListView.as_view(), name='files'),   
)



