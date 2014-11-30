from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.core.exceptions import ImproperlyConfigured
import autocomplete_light


autocomplete_light.autodiscover()
admin.autodiscover()


urlpatterns = patterns('',
    url(r'', include('home.urls')),
    url(r'', include('contact.urls')),
    url(r'', include('social.apps.django_app.urls', namespace='social')),
    url(r'', include('lscdsUser.urls')),
    url(r'^admin/', include(admin.site.urls)), 
    url(r'^accounts/',include('registration.backends.default.urls')),
    url(r'^weblog/', include('zinnia.urls',namespace='zinnia')),
    url(r'^comments/', include('django_comments.urls')),  
    url(r'^events/', include('chance.urls',namespace='chance')),
    url(r'^autocomplete/', include('autocomplete_light.urls')),
    (r'^gallery/', include('imagestore.urls', namespace='imagestore')),

    ) 

if settings.DEBUG:
    urlpatterns += patterns('',
                            (r'^' + settings.MEDIA_URL[1:] + '(?P<path>.*)$', 'django.views.static.serve',
                             {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
                            )
    try:
        urlpatterns += staticfiles_urlpatterns()
    except ImproperlyConfigured:
        pass
