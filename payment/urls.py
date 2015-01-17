from django.conf.urls import patterns, include, url
from payment.views import event_payment
urlpatterns = patterns('',
    url(r'^event-payment/$',event_payment,name='payment'),  
    (r'^paypal/', include('paypal.standard.ipn.urls')),
)
