from django.conf.urls import patterns, include, url
from django.conf import settings
from alumni.views import linkedin_authentication,linkedin_callback,rsvp_view,\
                         GuestUdateView,LscdsExecUdateView,AluminiRegistrationListView

urlpatterns = patterns('',
                 url('^alumni-reception-list/$',
                      AluminiRegistrationListView.as_view(),name='guest-list'),
                    url('^guest/rsvp/(?P<pk>[\w-]+)/(?P<event>[\w-]+)/$',  GuestUdateView.as_view(),name='guest-rsvp'),
                    url('^alumni/rsvp/(?P<pk>[\w-]+)/(?P<event>[\w-]+)/$', LscdsExecUdateView.as_view(),name='alumni-rsvp'),  
                    url(r'^alumin-reception/rsvp/(?P<rsvp_code>[-\w]+)/$',rsvp_view, name='rsvp'),
                    url(r'^linkedin/$', linkedin_authentication, name='lnin'),
                    url(r'^auth/linkedin/callback/$', linkedin_callback, name='linkin_callback'),                    
                    )
