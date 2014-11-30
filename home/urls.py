from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
urlpatterns = patterns('',
url(r'^$', TemplateView.as_view(template_name="home/index.html"),name="home"),
url(r'^about$', TemplateView.as_view(template_name="home/about.html"),name="about"),

)

