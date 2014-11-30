from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
urlpatterns = patterns('',
#url(r'^$', TemplateView.as_view(template_name="home/index.html"),name="home"),
url(r'^contact$', TemplateView.as_view(template_name="contact/contact.html"),name="contact"),
)

