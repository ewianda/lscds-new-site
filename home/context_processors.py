from event.models import Event,EventType
from zinnia.models.entry import Entry
from photologue.models import Gallery
from django.utils import timezone

def latest(request):
   try:
         event= Event.objects.filter(starts__gte = timezone.now())
   except Event.DoesNotExist:
        event = None
   try:
         eventtype= EventType.objects.all()
   except EventType.DoesNotExist:
        eventtype = None



   entry = Entry.published.all()[:2]
   try:
       photos = Gallery.objects.all().latest()
   except Gallery.DoesNotExist:
         photos = None
   

   return {'context_eventtype':eventtype,'context_event':event,'context_photos':photos,'context_blog':entry}

