from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from registration.users import UserModel, UserModelString
from ckeditor.fields import RichTextField
from django.db.models.query import QuerySet
from django.db.models import Q,Count
User=UserModel()


UPLOAD_TO = getattr(settings, 'PRESENTERS_UPLOAD_TO', 'presenters')
UPLOAD_BANNER_TO = getattr(settings, 'UPLOAD_BANNER_TO', 'banners')

class EventType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    location = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=100)
    def get_events(self):
        return self.event_type.select_related()
    

    def __unicode__(self):
        return self.name
   
    
    
# First, define the Manager subclass.

class EventQuerySet(QuerySet):
    def user_nr(self,user):
        return self.filter(event_type_id=1,starts__gte = timezone.now(),status="publish"). \
                         filter(event_round_table__round_table_registrations__student=user).\
                         annotate(dcount=Count('event_type'))

    def user_open_nr(self,user):
        return self.filter(event_type_id=1,starts__gte = timezone.now(),status="publish"). \
                         exclude(event_round_table__round_table_registrations__student=user)
    
    def user_events(self,user):
        return self.filter(starts__gte = timezone.now(),status="publish",registrations__owner=user).\
                           exclude(event_type_id=1)

    def user_open_events(self,user):
        return self.filter(starts__gte = timezone.now(),status="publish").\
                           exclude(event_type_id=1).\
                                  exclude(registrations__owner=user)
    def user_event_history(self,user):
        return self.filter(Q(registrations__owner=user)|Q(event_round_table__round_table_registrations__student=user)).\
                          filter(starts__lte = timezone.now(),status="publish").\
                                annotate(dcount=Count('event_type'))              
                                  
    
    
class EventManager(models.Manager):
       def get_query_set(self):
           return EventQuerySet(self.model, using=self._db)
       def user_nr(self,user):
           return self.get_query_set().user_nr(user)
       def user_open_nr(self,user):
           return self.get_query_set().user_open_nr(user)
    
       def user_events(self,user):
           return self.get_query_set().user_events(user)

       def user_open_events(self,user):
            return self.get_query_set().user_open_events(user)
       
       def user_event_history(self,user):
           return self.get_query_set().user_event_history(user)

STATUS = (
    ('Draft', 'draft'),
    ('Publish', 'publish'),

)
class Event(models.Model):
    event_type = models.ForeignKey(EventType, related_name='event_type')
    name = models.CharField(max_length=255)
    location = models.CharField(max_length=255, null=True, blank=True)
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    starts = models.DateTimeField()
    ends = models.TimeField()
    registration_limit = models.PositiveSmallIntegerField(null=True,
            blank=True, default=0)
    slug = models.SlugField(max_length=100)
    status = models.CharField(max_length=40, choices=STATUS)
    objects = EventManager()
    def get_talks(self):
        return self.event.select_related('presenter').all()
    def get_round_table(self):
        return self.event_round_table.all()
    def get_round_table_registration(self):
        return self.event.select_related('round_table_registrations') 

    def __unicode__(self):
        return self.name
    
    @models.permalink
    def get_absolute_url(self):
        return 'event:event-detail', (), {'slug': self.slug}
       

    @property
    def registration_open(self):
        if self.registration_start < timezone.now() <  self.registration_end:
            if self.registration_limit == 0 or self.registrations.count() < self.registration_limit:
               return True
            else:
                return False
        else:
          return False 
        
        



class Presenter(models.Model):
    name = models.CharField(max_length=255)
    qualification = models.CharField(max_length=255)
    alumni = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    email = models.EmailField(verbose_name='email address',
        max_length=255)
    image = models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    biography = RichTextField(blank=True, null=True)
    def __unicode__(self):
        return self.name



class Talk(models.Model):
    event = models.ForeignKey(Event, related_name='event')
    title = models.CharField(max_length=255, db_index=True)
    presenter = models.ForeignKey(Presenter)
    description = RichTextField(blank=True, null=True)
  
class EventFee(models.Model):
    event = models.ForeignKey(Event, related_name='fee_options')
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=65,decimal_places=2)

    def __unicode__(self):
        return u'%s at %s' % (self.name, self.event.name,)




class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations')
    owner = models.ForeignKey(User, related_name='+', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.owner,)

class RoundTable(models.Model):
    event = models.ForeignKey(Event, related_name='event_round_table')
    title = models.CharField(max_length=255, db_index=True)
    guest = models.ForeignKey(Presenter)
    description = RichTextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    table_limit = models.PositiveSmallIntegerField()
    slug = models.SlugField(max_length=16, null=True, blank=True)
    @property
    def registration_open(self):
        return self.round_table_registrations.count() < self.table_limit
    @property
    def get_spots(self):
        return self.table_limit -  self.round_table_registrations.count() 

    def __unicode__(self):
        return u'Round Table for  %s ' % (self.guest,)

class RoundTableRegistration(models.Model):
    round_table = models.ForeignKey(RoundTable, related_name='round_table_registrations', 
          error_messages={'unique': u'You have already registered for this event'}  )
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    student =  models.ForeignKey(User, related_name='my_round_table')
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)
    @property
    def event(self):
        return self.round_table.event
    class Meta:
        ordering = ('created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.student,)
    
    
class EventBanner(models.Model):
    eventtype = models.ForeignKey(EventType, related_name='event_type_banner')
    banner = models.ImageField(_('image'), upload_to=UPLOAD_BANNER_TO,
        help_text=_('Pre-process your banner for best quality. 1000x400 px is desired '))
    link = models.URLField(help_text=_('Link to the corresponding event'),blank=True, null=True)
    position = models.PositiveSmallIntegerField(max_length=10, default=1,help_text=_('First 4 banners will be displayed'),unique=True)
    def admin_image(self):
        return '<img width = "200" src="%s"/>' % self.banner.url
    admin_image.allow_tags = True
    
    
    def __unicode__(self):
        return self.eventtype.name
    class Meta:
        ordering = ('position',)

