from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.translation import ugettext_lazy as _

class AlumniTab(models.Model):
    name = models.CharField(max_length=255,unique=True)
    description = RichTextField(blank=True, null=True)
    slug = models.SlugField(max_length=40)
    @models.permalink
    def get_absolute_url(self):
         return 'alumni_tab',(),{'slug': self.slug}
         
    def __unicode__(self):
        return self.name