from django.conf.urls import patterns, include, url
from payment.views import event_payment,membership_payment
urlpatterns = patterns('',
     
    url(r'^payment/membership-payment/$', membership_payment ,name='membership-payment'),     
    url(r'^event-payment/$',event_payment,name='payment'),
    (r'^paypal/', include('paypal.standard.ipn.urls')),
)
