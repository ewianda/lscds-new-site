from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic import TemplateView
 
from lscdsUser.views import *

admin.autodiscover()
urlpatterns = patterns('',
    url(r'^web-unsubscribe$', WebUnsubscribeView.as_view(), name='web-unsubscribe'),
    url(r'^unsubscribe/(?P<pk>\w+)/(?P<first_name>\w+)/(?P<last_name>\w+)/$',
                     unsubscribe, name='unsubscribe'),
  
    url(r'^mailing-list-confirmation/$',
             TemplateView.as_view(template_name="mailinglist/mailing_confirmation.html"),
                  name='mailing-list-confirmation'),
 
    url(r'^ajax_mailing_list/$', ajax_mailing_list, name='ajax_mailing_list'),
    url(r'^mailing_list-form/$', MailingListView.as_view(), name='mailing_list-form'),
     url(r'^mailing_list/(?P<key>\w+)/$', mailing_list, name='mailing_list'),
    url(r'^upload-avatar/$', upload_file, name='upload-avatar'),
    url(r'^our-team/$', ExecListView.as_view(), name='exec'),
    url(r'^first-login/$', first_login, name='first-login'),
     url(r'^profile-uoft-email-verification/$', UHMVerificationView.as_view(), name='uoft-email-verification'),
     url(r'^unh-email/verify/(?P<verify_key>\w+)/$',
                           UHMVerifyView.as_view(),
                           name='uhn_verify'),
     url(r'^profile-event/$', event_view, name='profile-event'),
     url(r'^cd-registration/$', cd_registration, name='cd-registration'),
     url(r'^seminar-series-registration/$', ss_registration, name='ss-registration'),
     url(r'^network-reception-registration/$', nr_registration, name='nr-registration'),
     url(r'^profile-event-registration/$', registration_view, name='profile-event-registration'),
     url(r'^profile-notification/$', login_required(TemplateView.as_view(template_name="profile-notification.html")),
                                                    name='profile-notification'),

    url(r'^profile/$', UserUpdateView.as_view(), name='profile'),


     url(r'^email/$', require_email, name='require_email'),
     url(r'^complete_information/$', social_extra_data, name='social_extra_data'),
     url(r'^accounts/password/reset/$',
                           auth_views.password_reset,
                           {'post_reset_redirect': reverse_lazy('auth_password_reset_done'), \
                           },
                           name='password_reset'),
                       
     url(r'^password/reset/confirm-3/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$',
                           auth_views.password_reset_confirm,
                           {'post_reset_redirect': reverse_lazy('auth_password_reset_complete'),\
                           },
                           name='password_reset_confirm'),
                       
                                               
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


