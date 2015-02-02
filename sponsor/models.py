from django.db import models
from ckeditor.fields import RichTextField
from django.conf import settings
from event.models import Event
from django.utils.translation import ugettext_lazy as _
UPLOAD_TO = getattr(settings, 'PRESENTERS_UPLOAD_TO', 'sponsors')
class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    url = models.URLField()
    image = models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    class Meta:
        ordering=('name',)
    def __unicode__(self):
        return self.name


class EventSponsor(models.Model):
    event = models.ForeignKey(Event, related_name='sponsor')
    name = models.CharField(max_length=255)
    description = RichTextField(blank=True, null=True)
    url = models.URLField()
    image = models.ImageField(_('image'), blank=True,upload_to=UPLOAD_TO,
        help_text=_('Used for illustration.'))
    class Meta:
        ordering=('name',)
    def __unicode__(self):
        return self.name


