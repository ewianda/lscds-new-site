from django.conf.urls import patterns, include, url
from lscdsUser.views import LSCDSRegistrationView,require_email,social_extra_data,UserUpdateView,LSCDSActivationView,event_view, registration_view
from django.views.generic import TemplateView 
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Overide the Registration URL in registration.backends.default
     url(r'^profile-event/$',event_view, name='profile-event'),
     url(r'^profile-event-registration/$',registration_view, name='profile-event-registration'),
     url(r'^profile-notification/$',TemplateView.as_view(template_name="profile-notification.html"), name='profile-notification'),

    url(r'^profile/$',UserUpdateView.as_view(), name='profile-update'),


     url(r'^email/$', require_email, name='require_email'),
     url(r'^complete_information/$', social_extra_data, name='social_extra_data'),

    url(r'^accounts/register/$',
                          LSCDSRegistrationView.as_view(),
                           name='registration_register'),
    url(r'^login/',
        'django.contrib.auth.views.login',
        name='login'),
     url(r'^accounts/activate/(?P<activation_key>\w+)/$',
                           LSCDSActivationView.as_view(),
                           name='registration_activate'),

     url(r'^accounts/',
        include('registration.backends.default.urls')),

     )


