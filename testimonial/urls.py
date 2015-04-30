from django.conf.urls import patterns, url
from testimonial.views import TestimonialListView

urlpatterns = patterns('',
   url(r'^testimonials/$',TestimonialListView.as_view(), name='testimonial-list'),
  
)



