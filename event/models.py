from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from registration.users import UserModel, UserModelString
from ckeditor.fields import RichTextField

User=UserModel()


UPLOAD_TO = getattr(settings, 'PRESENTERS_UPLOAD_TO', 'presenters')
class EventType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    location = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=100)
    def get_events(self):
        return self.event_type.select_related()
    

    def __unicode__(self):
        return self.name

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
    def get_talks(self):
        return self.event.select_related('presenter')
    def get_round_table(self):
        return self.event_round_table.all()
    def get_round_table_registration(self):
        return self.event.select_related('round_table_registrations') 

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('event:event-detail',kwargs={'pk': self.pk})

    @property
    def registration_open(self):
        return self.registration_limit == 0 or \
            self.registrations.count() < self.registration_limit and \
            self.registration_start > timezone.now()



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

