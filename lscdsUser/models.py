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
from django.conf import settings


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




class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),date_joined=now,
        
        )

        user.set_password(password)
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
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now) 
    is_admin = models.BooleanField(_('Is Admin'), default=False)

    university = models.ForeignKey(University, max_length=40, null=True,)
    faculty = models.ForeignKey(Faculty,max_length=40, null=True,)
    department = models.ForeignKey(Department,max_length=40, null=True,)
    degree =  models.ForeignKey(Degree,max_length=40, null=True,)
    relationship =  models.CharField(max_length=40, choices=RELATIONSHIP_CHOICES,default='Student')
    mailinglist =  models.BooleanField( default=True)
    status =  models.CharField(max_length=40, choices=STATUS_CHOICES)
    avatar =  models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    gender =  models.CharField(max_length=10, choices=GENDER_CHOICES)
    service = models.CharField(max_length=30, blank=True)


    objects =MyUserManager()

    USERNAME_FIELD = 'email'
    #REQUIRED_FIELDS = ['date_of_birth']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True


