from django.db import models
from ckeditor.fields import RichTextField
# Create your models here.
from django.utils.translation import ugettext_lazy as _
class LscdsEmail(models.Model):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    def __unicode__(self):
        return self.email
    
class EmailTemplate(models.Model):
      template = models.CharField(_('Template name'),max_length=64)
      content = RichTextField()
      
      def __unicode__(self):
        return self.template
      