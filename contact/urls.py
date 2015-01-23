from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from contact.views import ContactView
urlpatterns = patterns('',
#url(r'^$', TemplateView.as_view(template_name="home/index.html"),name="home"),
url(r'^contact$', ContactView.as_view(),name="contact"),
)

