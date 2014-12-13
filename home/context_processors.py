from event.models import Event
from zinnia.models.entry import Entry
from photologue.models import Gallery
def latest(request):
   try:
         event= Event.objects.latest('starts')
   except Event.DoesNotExist:
        event = None
   entry = Entry.published.all()[:2]
   photos = entry = Gallery.objects.all().latest()
   return {'context_event':event,'context_photos':photos,'context_blog':entry}

