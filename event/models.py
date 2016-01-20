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
from lscdsUser.models import LscdsExec
from lscds_site.utils import send_event_register_mail
        






UPLOAD_TO = getattr(settings, 'PRESENTERS_UPLOAD_TO', 'presenters')
UPLOAD_BANNER_TO = getattr(settings, 'UPLOAD_BANNER_TO', 'banners')

class EventType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    location = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=100,unique=True)
    def get_events(self):
        return self.event_type.select_related()


    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'event:event-type-detail', (), {'slug': self.slug}

# First, define the Manager subclass.

class EventQuerySet(QuerySet):
    # Get career day event registration for a particular user
    def user_cd(self,user):
        return self.filter(event_type_id=2,starts__gte = timezone.now(),status="publish"). \
                         filter(event_pannels__cd_registration__student=user).\
                         annotate(dcount=Count('event_type'))

    def user_open_cd(self,user):
        return self.filter(event_type_id=2,starts__gte = timezone.now(),status="publish"). \
                         exclude(event_pannels__cd_registration__student=user)
    
    
    
    def user_nr(self,user):
        return self.filter(event_type_id=1,starts__gte = timezone.now(),status="publish"). \
                         filter(event_round_table__round_table_registrations__student=user).\
                         annotate(dcount=Count('event_type'))

    def user_open_nr(self,user):
        return self.filter(event_type_id=1,starts__gte = timezone.now(),status="publish"). \
                         exclude(event_round_table__round_table_registrations__student=user)

    def user_events(self,user):
        return self.filter(starts__gte = timezone.now(),status="publish",registrations__owner=user).\
                     exclude(event_type_id=4)
                           

    def user_open_events(self,user):
        return self.filter(starts__gte = timezone.now(),status="publish").exclude(registrations__owner=user).\
                    exclude(event_type_id=4)
    
    def user_event_history(self,user):
        return self.filter(Q(registrations__owner=user)|Q(event_round_table__round_table_registrations__student=user)).\
                          filter(starts__lte = timezone.now(),status="publish").\
                                annotate(dcount=Count('event_type'))



class EventManager(models.Manager):
       def get_query_set(self):
           return EventQuerySet(self.model, using=self._db)
       def user_cd(self,user):
           return self.get_query_set().user_cd(user)
       def user_open_cd(self,user):
           return self.get_query_set().user_open_cd(user)
       
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
    event_information = RichTextField(blank=True, null=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    registration_start = models.DateTimeField()
    registration_end = models.DateTimeField()
    starts = models.DateTimeField()
    ends = models.TimeField()
    registration_limit = models.PositiveSmallIntegerField(null=True,
            blank=True, default=0)
    none_u_of_t_limit =  models.PositiveSmallIntegerField(null=True,
            blank=True, default=0)
    
    slug = models.SlugField(max_length=100,unique=True)
    status = models.CharField(max_length=40, choices=STATUS)
    objects = EventManager()
    
    class Meta:
        ordering = ('-starts',)
    
    def get_alumi(self):
       return  self.alumniEvent.all().filter(alumni__active=False)
    def get_exec(self):
        return  self.alumniEvent.all().filter(alumni__active=True)
    
  
    def get_talks(self):
        return self.event.select_related('presenter').all()
    def get_round_table(self):
        return self.event_round_table.all()
    
    def get_cd_pannels(self):
        return self.event_pannels.all()
    
    def get_round_table_registration(self):
        return self.event.select_related('round_table_registrations')
    def break_location(self):
        return self.location.replace(',','<br>')
    def get_companies(self):
        return self.company.all()

    @property
    def has_fee(self):
         return self.fee_options.all()[0].amount !=0

    def __unicode__(self):
        return self.name

    @models.permalink
    def get_absolute_url(self):
        return 'event:event-detail', (), {'slug': self.slug}
    def get_registration_url(self):
        if self.event_type.pk ==1:            
           return reverse('nr-registration')
        elif self.event_type.pk ==2:            
           return reverse('cd-registration')
        else:
           return reverse('ss-registration') 
    @property
    def registration_open_non_u_of_t(self): 
           if self.none_u_of_t_limit==0 or self.registrations.filter(owner__is_u_of_t=False).count()<self.none_u_of_t_limit:
               return True
           else:
              return False
    @property
    def registration_open(self):
        if self.registration_start < timezone.now() <  self.registration_end:
            if self.registration_limit == 0 or \
                self.registrations.count() < self.registration_limit:
               return True
            else:
                return False
        else:
          return False

class Presenter(models.Model):
    name = models.CharField(_('First name'),max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255 )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
 
    )
    qualification = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)  
    sector = models.CharField(max_length=255,blank=True, null=True) 
    image = models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    biography = RichTextField(blank=True, null=True)
    rsvp_code = models.CharField(_('Rsvp code'), max_length=255 ,blank=True, null=True)
    affiliation = models.CharField(_('Affiliation for old database'), max_length=32 ,blank=True, null=True)
    year  = models.DateField(_('Year for old database'), default=timezone.now)
    def full_name(self):
        return "%s %s" % (self.name,self.last_name)
        
    full_name.allow_tags = True
    
    def __unicode__(self):
        return "%s %s" % (self.name,self.last_name)
    class Meta:
        ordering = ('-email','name')
        verbose_name_plural = _("Event Guests and Presenters")
        
    def send_email(self,event):
        action="send"
        template = ["alumni/event_register_email.txt","alumni/event_register_email.txt"]
        return send_event_register_mail(self,action,event,template,request=None,round_table=None)
        
        

class Talk(models.Model):
    event = models.ForeignKey(Event, related_name='event')
    title = models.CharField(max_length=255, db_index=True)
    presenter = models.ForeignKey(Presenter)
    description = RichTextField(blank=True, null=True)
    class Meta:
        verbose_name_plural = _("Key note and Talks") 
        
class   MembershipFee(models.Model):
        amount = models.DecimalField(max_digits=65,decimal_places=2)
        def __unicode__(self):
            return u'Anual Membership Fee %s' % (self.amount,)
        
        
class EventFee(models.Model):
    event = models.ForeignKey(Event, related_name='fee_options')
    available = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=65,decimal_places=2)

    def __unicode__(self):
        return u'Fees for %s (amount=0 for free event)' % (self.event.name,)




class Registration(models.Model):
    event = models.ForeignKey(Event, related_name='registrations')
    owner = models.ForeignKey(User, related_name='+', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)
    attended =   models.BooleanField(default=False)
    def email(self):
        return self.owner.email    
        

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.owner,)
    
    
class CDPanelsQuerySet(QuerySet):
    def get_user_panels(self,user,event):
        reg1=self.filter\
                (cd_registration__student=user,\
                cd_registration__session=1, event_id=event.id)
        reg2=self.filter\
                (cd_registration__student=user,\
                cd_registration__session=2, event_id=event.id)         
        return reg1,reg2   
        
class CDPanelsManager(models.Manager):
       def get_query_set(self):
           return  CDPanelsQuerySet(self.model, using=self._db)
       def get_user_panels(self,user,event):
           return self.get_query_set().get_user_panels(user,event)

class CDPanels(models.Model): 
       name = models.CharField(max_length=255)
       event = models.ForeignKey(Event, related_name='event_pannels')
       panel_limit = models.PositiveSmallIntegerField()  
       room = models.CharField(max_length=255,blank=True, null=True)
       objects = CDPanelsManager()
       def get_panelists(self):
           return self.panelists.all()
       def __unicode__(self):
            return u'%s' % (self.name,)
        
       class Meta:
           ordering = ('event',)
           verbose_name_plural = _("Career Day Panels")
       def session_spot(self,session):
           return self.panel_limit -  self.cd_registration\
                                         .filter(session=session).count()
       def registration_open(self,session):
          return self.cd_registration\
                            .filter(session=session).count() < self.panel_limit                                  
                                         
                                         
class CDPanelist(models.Model):
       cdpanel = models.ForeignKey(CDPanels,related_name='panelists')
       panelist = models.ForeignKey(Presenter)  
        
class CDRegistration(models.Model):
    cd_pannel = models.ForeignKey(CDPanels, related_name='cd_registration',
          error_messages={'unique': u'You have already registered for this event'}  )
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    student =  models.ForeignKey(User, related_name='my_cd_pannel')    
    paid = models.BooleanField(default=False)
    session = models.PositiveSmallIntegerField(max_length=10,default=1)
    attended =   models.BooleanField(default=False)
    def department(self):
        return self.student.department
    def faculty(self):
        return self.student.faculty
    def degree(self):
        return self.student.degree
    @property
    def event(self):
        return self.cd_pannel.event
    class Meta:
        ordering = ('student',)

    def __unicode__(self):
        return u'%s' % (self.student,)
    
class RoundTableQuerySet(QuerySet):
    def get_user_rountable(self,user,event):
        reg1=self.filter\
                (round_table_registrations__student=user,\
                round_table_registrations__session=1, event_id=event.id)
        reg2=self.filter\
                (round_table_registrations__student=user,\
                round_table_registrations__session=2, event_id=event.id)         
        return reg1,reg2   
        
class RoundTableManager(models.Manager):
       def get_query_set(self):
           return  RoundTableQuerySet(self.model, using=self._db)
       def get_user_rountable(self,user,event):
           return self.get_query_set().get_user_rountable(user,event)
      
class RoundTable(models.Model):
    event = models.ForeignKey(Event, related_name='event_round_table')
    title = models.CharField(max_length=255, db_index=True)
    guest = models.ForeignKey(Presenter)    
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    table_limit = models.PositiveSmallIntegerField()    
    objects = RoundTableManager()
    
    def registration_open(self,session):
        return self.round_table_registrations\
                            .filter(session=session).count() < self.table_limit
    @property
    def get_spots(self):
        return self.table_limit -  self.round_table_registrations.count()
    def session_spot(self,session):
        return self.table_limit -  self.round_table_registrations\
                                         .filter(session=session).count()
    

    def __unicode__(self):
        return u'Round Table for  %s ' % (self.guest,)
    class Meta:
        ordering = ('guest__name',)
        verbose_name_plural = _("Network Reception Round Tables")
        
class RoundTableRegistration(models.Model):
    round_table = models.ForeignKey(RoundTable, related_name='round_table_registrations',
          error_messages={'unique': u'You have already registered for this event'}  )
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)
    student =  models.ForeignKey(User, related_name='my_round_table')
    fee_option = models.ForeignKey(EventFee, related_name='+', null=True,
            blank=True)
    paid = models.BooleanField(default=False)
    session = models.PositiveSmallIntegerField(max_length=10,default=1)
    attended =   models.BooleanField(default=False)
    def department(self):
        return self.student.department
    def faculty(self):
        return self.student.faculty 
    @property
    def event(self):
        return self.round_table.event
    class Meta:
        ordering = ('student',)

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
        
        
        
class AlumniRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='alumniEvent')
    alumni = models.ForeignKey(LscdsExec, related_name='+', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True) 
    plus_one = models.CharField(_('Guest info'), max_length=255 )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.alumni,) 
           
    def name(self):
        return "%s" % (self.alumni)
       
class GuestRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='guest_event')
    guest = models.ForeignKey(Presenter, related_name='+', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True) 
    
    plus_one = models.CharField(_('Name of plus one guest'), max_length=255 )

    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'Registration for %s ' % (self.guest)
    
    def name(self):
        return "%s" % (self.guest)
    
class AdditionalGuestRegistration(models.Model):
    event = models.ForeignKey(Event, related_name='additional_guest_event')
    name = models.CharField(_('First name'),max_length=255)
    last_name = models.CharField(_('Last name'), max_length=255 )
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
 
    )
    qualification = models.CharField(max_length=255,blank=True, null=True)
    position = models.CharField(max_length=255)
    company = models.CharField(max_length=255)  
    sector = models.CharField(max_length=255,blank=True, null=True) 
    created = models.DateTimeField(auto_now_add=True, editable=False,
            null=True, blank=True)     
    attending = models.BooleanField(default=True)   
    class Meta:
        ordering = ('-created',)

    def __unicode__(self):
        return u'%s %s' % (self.name,self.last_name)  
    
    def full_name(self):
        return "%s %s" % (self.name,self.last_name)
        
    full_name.allow_tags = True 
    
    def send_email(self,event):
        action="send"
        template = ["alumni/event_register_email.txt","alumni/event_register_email.txt"]
        return send_event_register_mail(self,action,event,template,request=None,round_table=None)
    
UPLOAD_TO_COMPANY = getattr(settings, 'COMPANY_UPLOAD_TO', 'company')   
class EventCompany(models.Model):
    event = models.ForeignKey(Event, related_name='company')
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    link = models.URLField()
    image = models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO_COMPANY,
        help_text=_('Picture'))
    class Meta:
        ordering=('name',)
        verbose_name_plural = _("Career Day Companies")          
    def __unicode__(self):
        return self.name
    
    
 
 
    
'''
class Schedule(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)    
    class Meta:
        ordering=('name',)
       
          
    def __unicode__(self):
        return self.name 
    
       
class EventSchedule(models.Model):
    event = models.ForeignKey(Event, related_name='event_schedule')
    schedule = models.ForeignKey(Schedule, related_name='+')
    def __unicode__(self):
        return str(self.event)
    
'''  
    
