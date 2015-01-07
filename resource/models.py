from django.db import models

# Create your models here.
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings
from django.core.urlresolvers import reverse

from ckeditor.fields import RichTextField


class ResourceType(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=40)
    def get_events(self):
        return self.event_type.select_related()   

    def __unicode__(self):
        return self.name

class Resource(models.Model):
    event_type = models.ForeignKey(ResourceType, related_name='resource_type')
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, null=True, blank=True)
    description = RichTextField(blank=True, null=True)
    date_posted = models.DateTimeField(default = timezone.now)
    slug = models.SlugField(max_length=16, null=True, blank=True)
    link = models.URLField()
    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resource:resource-detail',kwargs={'pk': self.pk})


