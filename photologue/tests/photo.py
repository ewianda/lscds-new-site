import os

from django.conf import settings
from imagekit.cachefiles import ImageCacheFile

from ..models import Image, Photo, PHOTOLOGUE_DIR
from .factories import LANDSCAPE_IMAGE_PATH, PhotoFactory
from .helpers import PhotologueBaseTest
from photologue.processors import PhotologueSpec


class PhotoTest(PhotologueBaseTest):

    def test_new_photo(self):
        self.assertEqual(Photo.objects.count(), 1)
        self.assertTrue(os.path.isfile(self.pl.image.path))
        self.assertEqual(os.path.getsize(self.pl.image.path),
                         os.path.getsize(LANDSCAPE_IMAGE_PATH))

    def test_remove_photo_file(self):
        photo = PhotoFactory(title='New Photo', title_slug='newphoto')
        image_path = photo.image.path
        self.assertTrue(os.path.isfile(image_path))
        photo.delete()
        self.assertFalse(os.path.isfile(image_path))


    def test_paths(self):
        self.assertEqual(os.path.normpath(str(self.pl.cache_path())).lower(),
                         os.path.normpath(os.path.join(settings.MEDIA_ROOT,
                                                       PHOTOLOGUE_DIR,
                                                       'photos',
                                                       'cache')).lower())
        self.assertEqual(self.pl.cache_url(),
                         settings.MEDIA_URL + PHOTOLOGUE_DIR + '/photos/cache')

    def test_count(self):
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 0)
        self.s.increment_count = True
        self.s.save()
        for i in range(5):
            self.pl.get_testPhotoSize_url()
        self.assertEqual(self.pl.view_count, 5)

    def test_precache(self):
        # set the thumbnail photo size to pre-cache
        self.s.pre_cache = True
        self.s.save()
        # make sure it created the file
        self.assertTrue(os.path.isfile(self.pl.get_testPhotoSize_filename()))
        self.s.pre_cache = False
        self.s.save()
        # clear the cache and make sure the file's deleted
        self.pl.clear_cache()
        self.assertFalse(os.path.isfile(self.pl.get_testPhotoSize_filename()))

    def test_accessor_methods_photosize(self):
        self.assertEqual(self.pl.get_testPhotoSize_photosize(), self.s)

    def test_accessor_methods_size(self):
        self.assertEqual(self.pl.get_testPhotoSize_size(),
                         Image.open(self.pl.get_testPhotoSize_filename()).size)

    def test_accessor_methods_url(self):
        generator = PhotologueSpec(photo=self.pl, photosize=self.s)
        cache = ImageCacheFile(generator)
        self.assertEqual(self.pl.get_testPhotoSize_url(),
                         cache.url)

    def test_accessor_methods_filename(self):
        generator = PhotologueSpec(photo=self.pl, photosize=self.s)
        cache = ImageCacheFile(generator)
        self.assertEqual(self.pl.get_testPhotoSize_filename(), cache.file.name)

