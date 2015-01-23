from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from home.views import HomeView
urlpatterns = patterns('',
url(r'^$', HomeView.as_view(template_name="home/index.html"),name="home"),
url(r'^about$', TemplateView.as_view(template_name="home/about.html"),name="about"),

)

