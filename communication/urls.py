from django.conf.urls import patterns, url
from communication.views import load_template,send_queue_emails
urlpatterns = patterns('',
    url(r'^load_template/$', load_template, name='load_template'), 
    url(r'^worker/$', send_queue_emails, name='task-queue'), 
    )
