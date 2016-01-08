from django.db import models
from django.utils.translation import ugettext_lazy as _
# Create your models here.
class LscdsLogo(models.Model):
    image = models.ImageField(_('logo'),upload_to='logo')    
    def __unicode__(self):
        return self.image.url