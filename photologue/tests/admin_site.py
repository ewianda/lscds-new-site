#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User
from django.test import RequestFactory
from photologue.admin import PhotoAdmin
from photologue.models import Photo
from photologue.tests.helpers import PhotologueBaseTest


class PhotoAdminTest(PhotologueBaseTest):

    def setUp(self):
        super(PhotoAdminTest, self).setUp()
        admin_site = AdminSite('Test Admin')
        self.photo_admin = PhotoAdmin(Photo, admin_site)
        self.user = User.objects.create_superuser('test1', 'test@example.com',
                                              'pass')
        self.factory = RequestFactory()
        self.request = self.factory.get('/fake/url')
        self.request.user = self.user

    def test_should_render_custom_template_on_changelist_view(self):
        response = self.photo_admin.changelist_view(self.request)
        self.assertIn('admin/photologue/photo/change_list.html', response.template_name)

    def test_should_render_custom_template_on_change_view(self):
        response = self.photo_admin.change_view(self.request, object_id=str(self.pl.id))
        self.assertIn('admin/photologue/photo/change_form.html', response.template_name)

    def test_should_have_size_on_context__change_view(self):
        response = self.photo_admin.change_view(self.request, object_id=str(self.pl.id))
        self.assertIn(self.s, response.context_data['sizes'])

    def test_should_redirect_to_thumb_image_get_on_photo_size_view(self):
        response = self.photo_admin.photo_size_view(self.request, object_id=str(self.pl.id), size=self.s.name)
        self.assertEqual(response.status_code, 301)
        self.assertEqual(dict(response.items())['Location'], self.pl.get_testPhotoSize_url())
