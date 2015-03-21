"""  
This code was copied from https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#a-full-example
Little modifications to accomodate the need for this site

Author Elvis Wianda

"""



import datetime
import hashlib
import random
import re

from sorl.thumbnail import ImageField

from ckeditor.fields import RichTextField
from django.conf import settings
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, \
    PermissionsMixin
from django.core.mail import EmailMultiAlternatives
from django.db import models
from django.template import Context, RequestContext, TemplateDoesNotExist
from django.template.loader import get_template, render_to_string
from django.utils import six, timezone
from django.utils.translation import ugettext_lazy as _
from institute.models import University, Faculty, Department, Degree
from lscds_site.utils import send_event_register_mail

UPLOAD_TO = getattr(settings, 'USERS_UPLOAD_TO', 'lscdsUsers')

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Secret', 'Secret'),
)

STATUS_CHOICES = (
    ('Full-time', 'Full-time'),
    ('Part-time', 'Part-time'),
    ('Other', 'Other'),
)

RELATIONSHIP_CHOICES = (
    ('Student', 'Student'),
    ('Executive', 'Executive'),
    ('Guest', 'Guest'),
)
UHN_EMAILS = ['mail.utoronto.ca', 'sickkids.ca', 'toronto.ca']

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class MyUserManager(BaseUserManager):
    def create_verify_key(self, user, uhn_email):
        """     
        The verify key for the user will be a
        SHA1 hash, generated from a combination of the ``User``'s
        email and a random salt.
        """
        salt = hashlib.sha1(six.text_type(random.random()).encode('ascii')).hexdigest()[:5]
        salt = salt.encode('ascii')
        email = user.email
        if isinstance(email, six.text_type):
            email = email.encode('utf-8')
        verify_key = hashlib.sha1(salt + email).hexdigest()
        user.verify_key = verify_key
        user.uhn_email = uhn_email
        user.save()
        return user
        
        
        
    def verify_user(self, verify_key):
        """
        Validate an verify key and activate the corresponding
        ``User`` if valid.
        If the key is valid and has not expired, return the ``User``
        after activating.
        If the key is not valid or has expired, return ``False``.
        If the key is valid but the ``User`` is already active,
        return ``False``.
        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        now = timezone.now()
        if now.day > 9:  # then we are in the same year as start of academic year
             year = now.year 
        else:
             year = now.year + 1  # set expiration for next year
        expiry_date = datetime.datetime(year, 9, 30)
        if SHA1_RE.search(verify_key):
            try:
                user = self.get(verify_key=verify_key)
            except self.model.DoesNotExist:
                return False
            user.is_u_of_t = True            
            user.expiry_date = expiry_date
            user.save()            
            return user
        return False
    
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        now = timezone.now()
        if now.day > 9:  # then we are in the same year as start of academic year
             year = now.year 
        else:
             year = now.year + 1  # set expiration for next year
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email), date_joined=now,
            expiry_date=datetime.datetime(year, 9, 30)
        )

        user.set_password(password)
        if email.split('@')[1] in str(UHNEmail.objects.all()):
           user.is_u_of_t = True
           user.save(using=self._db)
           return user
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password
        )
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user

class LscdsUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    uhn_email = models.EmailField(
        verbose_name='uhn email address',
        max_length=255,
    )
    expiry_date = models.DateField(_('Expiry date'), default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now) 
    is_admin = models.BooleanField(_('Is Admin'), default=False) 
    is_u_of_t = models.BooleanField(_('Active U of T student'), default=False)
    university = models.ForeignKey(University, max_length=40, null=True,)
    faculty = models.ForeignKey(Faculty, max_length=40, null=True,)
    department = models.ForeignKey(Department, max_length=40, null=True,)
    degree = models.ForeignKey(Degree, max_length=40, null=True,)
    relationship = models.CharField(max_length=40, choices=RELATIONSHIP_CHOICES, default='Student')
    mailinglist = models.BooleanField(default=True)
    status = models.CharField(max_length=40, choices=STATUS_CHOICES)
    avatar = ImageField(_('image'), blank=True, upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default='Secret')
    service = models.CharField(max_length=30, blank=True)
    verify_key = models.CharField(max_length=40)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return u'%s %s ' % (self.first_name, self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):  # __unicode__ on Python 2
        return u'%s %s ' % (self.first_name, self.last_name)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True
    def is_verified(self):
        return self.is_u_of_t and self.expiry_date > timezone.now().date()
    
    
    def send_verify_mail(self, site, uhn_email, request=None):
        
        email_dict = {}         
        if request is not None:
            email_dict = RequestContext(request, email_dict)
        subject = "Verify your University of Toronto email( or affiliated institution email)"
        email_dict = {
            "user": self,
            "verify_key": self.verify_key,
            "site": site,
        }
        message_txt = render_to_string('email/verify_email.txt', email_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [uhn_email])
        message_html = render_to_string('email/verify_email.html', email_dict)
        email_message.attach_alternative(message_html, 'text/html')
        email_message.send()
    def send_event_register_mail(self, action, event, site, request=None, round_table=None):        
        email_dict = {}         
        if request is not None:
            email_dict = RequestContext(request, email_dict)
        subject = "%s Event Registration" % (event)
        email_dict = {
            "event": event,
            "user": self,
            "site": site,
            "action": action,
        }
        if round_table is not None:
            rt1 = round_table[0]
            rt2 = round_table[1]
            email_dict['rt1'] = rt1
            email_dict['rt2'] = rt2
        email_ctx = Context(email_dict)
        txt = get_template('email/event_register_email.txt')
        html = get_template('email/event_register_email.html')
        message_txt = txt.render(email_ctx)
        message_html = html.render(email_ctx)       
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.email])
        
        email_message.attach_alternative(message_html, 'text/html')
        email_message.send()
    def send_event_modifiction_mail(self, event, site, request=None, round_table=None):        
        email_dict = {}         
        if request is not None:
            email_dict = RequestContext(request, email_dict)
        subject = "%s Event Registration" % (event)
        email_dict = {
            "user": self,
            "site": site,
             "event": event,
        }
        if round_table is not None:
            rt1 = round_table[0]
            rt2 = round_table[1]
            email_dict.append({'rt1':rt1, 'rt2':rt2})
        message_txt = render_to_string('email/event_modification_email.txt', email_dict)
        email_message = EmailMultiAlternatives(subject, message_txt, settings.DEFAULT_FROM_EMAIL, [self.email])
        message_html = render_to_string('email/event_modification_email.html', email_dict)
        email_message.attach_alternative(message_html, 'text/html')
        email_message.send()  
        
         
        
        
        
        
        
        
        
class UHNEmail(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = _("UHN Email")
    def __unicode__(self):
        return self.name




class OldlscdsUser(models.Model):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        blank=True, null=True
    )
    is_active = models.BooleanField(_('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    first_name = models.CharField(_('first name'), max_length=30, blank=True, null=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True, null=True)
    password = models.CharField(max_length=100, blank=True, null=True)
    raw_password = models.CharField(max_length=100, blank=True, null=True)
    middle_name = models.CharField(_('middle name'), max_length=30 , null=True, blank=True,)
    url = models.URLField(blank=True, null=True)
    # bio = RichTextField(blank=True, null=True)
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now) 
    mailinglist = models.BooleanField(default=True)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)
    def __unicode__(self):
        return u'%s %s ' % (self.first_name, self.last_name)
    
    def set_password(self, raw_password):
        from lscds_site.backend import make_pw_hash
        self.password = make_pw_hash(self.email, raw_password)

class LscdsExec(models.Model):
    user = models.OneToOneField(LscdsUser)
    position = models.CharField(_('Postion'), max_length=255)
    avatar = ImageField(_('Image'), blank=True, upload_to=UPLOAD_TO)
    start = models.DateField(_('From'), default=timezone.now)
    end = models.DateField(_('Year'), default=timezone.now)
    bio = RichTextField(blank=True, null=True)
    active = models.BooleanField(default=True)
    current_position = models.CharField(_('Current postion'), max_length=255, null=True, blank=True) 
    company = models.CharField(_('Company'), max_length=255, null=True, blank=True)
    rsvp_code = models.CharField(_('Rsvp code'), max_length=255 , blank=True, null=True)
    
    def admin_image(self):
        if self.avatar:
           return '<img width = "50" src="%s">' % self.avatar.url
        else: 
           return '<img width = "200" scr="http://placehold.it/200x100&text=Image" >'
       
    admin_image.allow_tags = True
    
    def __unicode__(self):
        return str(self.user)
    class Meta:
        verbose_name_plural = _("Execs and Alumni")
    
    def send_email(self,event):
        action="send"
        template = ["alumni/event_register_email.txt","alumni/event_register_email.txt"]
        return send_event_register_mail(self.user,action,event,template,request=None,round_table=None)
        
        
         
class MailingList(models.Model):   
      email = models.EmailField(
        verbose_name='email address',
        max_length=255, unique=True,
        )
      first_name = models.CharField(_('first name'), max_length=30)
      last_name = models.CharField(_('last name'), max_length=30)
      def __unicode__(self):
        return u'%s %s ' % (self.first_name, self.last_name)
      
      
      
      
      
      
      
      
      
      
    
    
    
    
