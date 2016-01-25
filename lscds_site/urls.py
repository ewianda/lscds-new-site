from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.exceptions import ImproperlyConfigured
#import autocomplete_light
from rest_framework import routers
from api import apiviews
from rest_framework.authtoken import views as drf_views

#autocomplete_light.autodiscover()
admin.autodiscover()


router = routers.DefaultRouter()
router.register(r'users', apiviews.UserViewSet)
router.register(r'users', apiviews.UserViewSet)


urlpatterns = patterns('',
    url(r'^api/', include(router.urls)),    
    url(r'^api/profile', apiviews.UserProfileApi.as_view(),name='api-profile'),    
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')), 
    url(r'^api-token-auth/', drf_views.obtain_auth_token),                 
    url(r'', include('communication.urls')),                  
    url(r'', include('alumni.urls')),                   
    url(r'', include('home.urls')),
    url(r'', include('testimonial.urls')),
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
(r'^search/', include('googlesearch.urls')),

    ) 


