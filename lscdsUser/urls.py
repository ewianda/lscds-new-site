from django.conf.urls import patterns, include, url
from lscdsUser.views import LSCDSRegistrationView,require_email,social_extra_data
from django.views.generic import TemplateView 
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Overide the Registration URL in registration.backends.default 
     url(r'^email/$', require_email, name='require_email'),
     url(r'^complete_information/$', social_extra_data, name='social_extra_data'),

    url(r'^accounts/register/$',
                          LSCDSRegistrationView.as_view(),
                           name='registration_register'),
       url(r'^accounts/profile/',
        TemplateView.as_view(template_name='profile.html'),
        name='profile'),

    url(r'^login/',
        'django.contrib.auth.views.login',
        name='login'),
     url(r'^accounts/',
        include('registration.backends.default.urls')),

     )


