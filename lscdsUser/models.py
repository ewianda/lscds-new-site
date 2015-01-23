"""  
This code was copied from https://docs.djangoproject.com/en/1.5/topics/auth/customizing/#a-full-example
Little modifications to accomodate the need for this site

Author Elvis Wianda

"""



from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser,PermissionsMixin
)
from institute.models import (University,Faculty,Department, Degree)
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.utils import six
from django.conf import settings
import datetime
from django.core.mail import EmailMultiAlternatives
from django.template import RequestContext, TemplateDoesNotExist
import hashlib
import random
import re
from django.template.loader import render_to_string

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
UHN_EMAILS = ['mail.utoronto.ca','sickkids.ca','toronto.ca']

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class MyUserManager(BaseUserManager):
    def create_verify_key(self,user):
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
        verify_key = hashlib.sha1(salt+email).hexdigest()
        user.verify_key=verify_key
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
        if now.day > 9: # then we are in the same year as start of academic year
             year = now.year 
        else:
             year = now.year +1 # set expiration for next year
        expiry_date = datetime.datetime(year,9,30)
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
        if now.day > 9: # then we are in the same year as start of academic year
             year = now.year 
        else:
             year = now.year +1 # set expiration for next year
        if not email:
            raise ValueError('Users must have an email address')
        
        user = self.model(
            email=self.normalize_email(email),date_joined=now,
            expiry_date = datetime.datetime(year,9,30)
        )

        user.set_password(password)
        if email.split('@')[1] in str(UHNEmail.objects.all()):
           user.is_u_of_t = True
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
    expiry_date = models.DateField(_('Expiry date'),default=timezone.now)
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=30 )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now) 
    is_admin = models.BooleanField(_('Is Admin'), default=False) 
    is_u_of_t = models.BooleanField(_('Active U of T student'), default=False)
    university = models.ForeignKey(University, max_length=40, null=True,)
    faculty = models.ForeignKey(Faculty,max_length=40, null=True,)
    department = models.ForeignKey(Department,max_length=40, null=True,)
    degree =  models.ForeignKey(Degree,max_length=40, null=True,)
    relationship =  models.CharField(max_length=40, choices=RELATIONSHIP_CHOICES,default='Student')
    mailinglist =  models.BooleanField( default=True)
    status =  models.CharField(max_length=40, choices=STATUS_CHOICES)
    avatar =  models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    gender =  models.CharField(max_length=10, choices=GENDER_CHOICES,default='Secret')
    service = models.CharField(max_length=30, blank=True)
    verify_key = models.CharField(max_length=40)

    objects =MyUserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return u'%s %s ' % (self.first_name,self.last_name)

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __unicode__(self):              # __unicode__ on Python 2
        return u'%s %s ' % (self.first_name,self.last_name)

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
    
    
    def send_verify_mail(self, site,uhn_email,request=None):
        
        email_dict={}         
        if request is not None:
            email_dict = RequestContext(request, email_dict)
        subject="Verify your UTOR or UHN email"
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
        
        
class UHNEmail(models.Model):
    name = models.CharField(max_length=100)
    class Meta:
        verbose_name = _("UHN Email")
    def __unicode__(self):
        return self.name
