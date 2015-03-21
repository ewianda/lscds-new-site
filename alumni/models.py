from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from event.models import Event
# Create your models here.
class Alumni(models.Model):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,blank=True, null=True
 
    ) 
    last_updated = models.DateField(_('Last Updated'),default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=255)
    last_name = models.CharField(_('last name'), max_length=255 )
    
    position = models.CharField(_('Position'), max_length=255, blank=True, null=True)
    company = models.CharField(_('Comapany'), max_length=255 ,blank=True, null=True)
    rsvp_code = models.CharField(_('Rsvp code'), max_length=255 ,blank=True, null=True)
    
    class Meta:
        ordering = ('-email','first_name')
        
        
    def __unicode__(self):              # __unicode__ on Python 2
        return u'%s %s ' % (self.first_name,self.last_name)
    
    
class AlumniRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='alumni_event')
    alumni = models.ForeignKey(Alumni, related_name='+', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True) 

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.alumni,)