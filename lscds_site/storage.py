import os, re
from sorl.thumbnail.base import ThumbnailBackend
from django.template.defaultfilters import slugify
from django.conf import settings
from sorl.thumbnail.helpers import tokey, serialize

EXTENSIONS = {
    'JPEG': 'jpg',
    'PNG': 'png',
}


class SEOThumbnailBackend(ThumbnailBackend):
    """
    Custom backend for SEO-friendly thumbnail file names/urls.
    """
   
    def _get_thumbnail_filename(self, source, geometry_string, options):
        """
        Computes the destination filename.
        """
        key = tokey(source.key, geometry_string, serialize(options))
        # make some subdirs
        path = '%s/%s/%s' % (key[:2], key[2:4], key)
        return "%s%s.%s" % (settings.THUMBNAIL_PREFIX, path,
                            EXTENSIONS[options['format']])

