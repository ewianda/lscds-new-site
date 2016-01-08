from event.models import Event,EventType
from zinnia.models.entry import Entry
from photologue.models import Gallery
from testimonial.models import Testimonial
from logo.models import LscdsLogo

from django.utils import timezone
from datetime import datetime,timedelta
from django.conf import settings
from django.core.cache import cache
import twitter
from resource.models import (Resource, Jobs ,Files) 
from alumni.models import AlumniTab
def twitterAuthenticate():  
    consumer_key=settings.SOCIAL_AUTH_TWITTER_KEY
    consumer_secret=settings.SOCIAL_AUTH_TWITTER_SECRET
    access_token_key=settings.TWITTER_ACCESS_TOKEN_KEY
    access_token_secret=settings.TWITTER_ACCESS_TOKEN_SECRET     
    api = twitter.Api(consumer_key= consumer_key,consumer_secret= consumer_secret,\
                      access_token_key= access_token_key,\
                      access_token_secret= access_token_secret,cache=None)
    return api 
      


def latest_tweets( request ):
    tweets = cache.get('tweets')
    if tweets:
        return {"tweets": tweets}
    tweets=[]
    api = twitterAuthenticate()
   
    status=api.GetUserTimeline( settings.TWITTER_USER )[:2]
    for x in range(2):
        tweets.append({"id":status[x].id,"user":status[x].user.screen_name})     
    cache.set( 'tweets', tweets, settings.TWITTER_TIMEOUT )
    return {"tweets": tweets}



def latest(request):
   try:
         event= Event.objects.filter(starts__gte = timezone.now()-timedelta(hours=4),status = "publish").order_by('starts')
   except Event.DoesNotExist:
        event = None
   try:
         eventtype= EventType.objects.all()
   except EventType.DoesNotExist:
        eventtype = None


   try:
      entry = Entry.published.all()[:2]
   except Entry.DoesNotExist:
      entry = None
   try:
       photos = Gallery.objects.all().latest()
   except Gallery.DoesNotExist:
         photos = None
   try:
       jobs = Jobs.objects.all()[:2]
   except Jobs.DoesNotExist:
         jobs = None
         
   try:
       resources = Resource.objects.all()
   except Resoucres.DoesNotExist:
         resources = None

   try:
       alumni_tab = AlumniTab.objects.all()
   except AlumniTab.DoesNotExist:
         alumni_tab = None
   
   try:
       testimonial = Testimonial.objects.all()
   except Testimonial.DoesNotExist:
       testimonial = None
   try: 
      logo = LscdsLogo.objects.first()
   except  LscdsLogo.DoesNotExist:
       logo = None   




   return {'context_eventtype':eventtype,'context_event':event,\
           'context_photos':photos,'context_blog':entry,\
           'jobs':jobs,'context_resource':resources,\
           'context_alumni_tab':alumni_tab,"now":timezone.now()-timedelta(hours=4),
           'testimonies':testimonial,
           'logo': logo
           }

