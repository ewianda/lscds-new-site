from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField
UPLOAD_TO = getattr(settings, 'FILE_UPLOAD_TO', 'file_upload')

class Resource(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=40)
    @models.permalink
    def get_absolute_url(self):
         return 'resource:resources',(),{'slug': self.slug}
         
    def __unicode__(self):
        return self.name

class Jobs(models.Model):   
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default = timezone.now)
    slug = models.SlugField(max_length=40,unique=True)    
    link = models.URLField()
    class Meta:
        ordering = ['-date_posted']
        
    def __unicode__(self):
        return self.title
    @models.permalink
    def get_absolute_url(self):        
        return 'resource:job',(),{'slug': self.slug}


class Files(models.Model):
    name = models.CharField(max_length=255)    
    file = models.FileField(upload_to=UPLOAD_TO)
    def __unicode__(self):
        return self.name
    
    
    
    