from django.db import models
from event.models import Event
from ckeditor.fields import RichTextField
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class Testimonial(models.Model): 
      testimony = RichTextField()  
      name = models.CharField(_('Name of Participant'), max_length=30)
      event = models.ForeignKey(Event,related_name='+')
      def __unicode__(self):
        return u'%s' % (self.name) 