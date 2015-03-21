from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.exceptions import ImproperlyConfigured
#import autocomplete_light


#autocomplete_light.autodiscover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('communication.urls')),                  
    url(r'', include('alumni.urls')),                   
    url(r'', include('home.urls')),
    url(r'^events/', include('event.urls', namespace='event')),
    url(r'^resources/', include('resource.urls', namespace='resource')),
    url(r'', include('payment.urls', namespace='paypal')),
    url(r'^our-sponsors/', include('sponsor.urls', namespace='sponsors')),
    url(r'', include('contact.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('lscdsUser.urls')),
    url(r'^admin-lsdcds-main-page/', include(admin.site.urls)), 
    url(r'^accounts/',include('registration.backends.default.urls')),
    url(r'^weblog/', include('zinnia.urls',namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),  
   # url(r'^autocomplete/', include('autocomplete_light.urls')),
    url(r'^photologue/', include('photologue.urls')),
    (r'^ckeditor/', include('ckeditor.urls')),
     url(r'^faq/', include('simple_faq.urls')),
     #url(r'^support/', include('live_support.urls')),
       (r'^adminactions/', include('adminactions.urls')),


    ) 


