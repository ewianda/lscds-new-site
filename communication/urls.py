from django.conf.urls import patterns, url
from communication.views import *
urlpatterns = patterns('',
    url(r'^load_template/$', load_template, name='load_template'), 
    url(r'^worker/$', send_queue_emails, name='task-queue'),
    url(r'^worker2/$', send_queue_emails2, name='task-queue2'),
    url(r'^download_listserve/$', export_listserv, name='download-listserve'),
    url(r'^send-list-serve-email/$', send_listserv_email , name='send-listserve-email'),
    )
