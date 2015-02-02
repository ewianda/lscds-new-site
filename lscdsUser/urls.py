from django.conf.urls import patterns, include, url
from lscdsUser.views import UHMVerificationView,UHMVerifyView,\
 LSCDSRegistrationView,require_email,social_extra_data,\
 UserUpdateView,LSCDSActivationView,event_view, \
 registration_view,ExecListView,upload_file,ajax_mailing_list,\
first_login 
 
from django.views.generic import TemplateView 
from django.contrib import admin
admin.autodiscover()
urlpatterns = patterns('',
    # Overide the Registration URL in registration.backends.default
    url(r'^ajax_mailing_list/$',ajax_mailing_list,name='ajax_mailing_list'),
    url(r'^upload-avatar/$',upload_file,name='upload-avatar'),
    url(r'^our-team/$',ExecListView.as_view(), name='exec'),
    url(r'^first-login/$',first_login,name='first-login'),
     url(r'^profile-uoft-email-verification/$',UHMVerificationView.as_view(), name='uoft-email-verification'),
     url(r'^unh-email/verify/(?P<verify_key>\w+)/$',
                           UHMVerifyView.as_view(),
                           name='uhn_verify'),
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


