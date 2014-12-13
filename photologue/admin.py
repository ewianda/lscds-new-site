from django.conf.urls import patterns, url
from django.contrib import admin
from django.http import HttpResponsePermanentRedirect
from django.utils.translation import ugettext_lazy as _
from django import forms
from django.conf import settings

from .models import Gallery, Photo, GalleryUpload, PhotoEffect, PhotoSize, \
    Watermark

USE_CKEDITOR = getattr(settings, 'PHOTOLOGUE_USE_CKEDITOR', False)

if USE_CKEDITOR:
    from ckeditor.widgets import CKEditorWidget


class GalleryAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        description = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Gallery


class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_added', 'photo_count', 'is_public')
    list_filter = ['date_added', 'is_public']
    date_hierarchy = 'date_added'
    prepopulated_fields = {'title_slug': ('title',)}
    filter_horizontal = ('photos',)
    form = GalleryAdminForm


class PhotoAdminForm(forms.ModelForm):
    if USE_CKEDITOR:
        caption = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Photo


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_taken', 'date_added', 'is_public', 'tags', 'view_count', 'admin_thumbnail')
    list_filter = ['date_added', 'is_public']
    search_fields = ['title', 'title_slug', 'caption']
    list_per_page = 20
    prepopulated_fields = {'title_slug': ('title',)}
    form = PhotoAdminForm

    fieldsets = (
        (None, {
            'fields': ('image', 'title', 'crop_from', 'caption')
        }),
        (_('Advanced options'), {
            'classes': ('collapse',),
            'fields': ('title_slug', 'effect', 'date_added', 'is_public', 'tags')
        }),
    )

    def get_urls(self):
        urls = super(PhotoAdmin, self).get_urls()
        my_urls = patterns('',
            url(r'^(?P<object_id>[0-9]+)/size/(?P<size>[\-\d\w]+)/$',
             self.admin_site.admin_view(self.photo_size_view),
             name='photologue-photo-size'
            )
        )
        return my_urls + urls

    def photo_size_view(self, request, object_id, size):
        obj = self.model.objects.get(id=object_id)
        return HttpResponsePermanentRedirect(obj._get_SIZE_url(size))


    def change_view(self, request, object_id, form_url='', extra_context=None):
        sizes = PhotoSize.objects.all()
        extra_context = {'sizes': sizes}
        return super(PhotoAdmin, self).change_view(request, object_id, form_url,
                                                   extra_context)


class PhotoEffectAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'color', 'brightness', 'contrast', 'sharpness', 'filters', 'admin_sample')
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        (_('Adjustments'), {
            'fields': ('color', 'brightness', 'contrast', 'sharpness')
        }),
        (_('Filters'), {
            'fields': ('filters',)
        }),
        (_('Reflection'), {
            'fields': ('reflection_size', 'reflection_strength', 'background_color')
        }),
        (_('Transpose'), {
            'fields': ('transpose_method',)
        }),
    )


class PhotoSizeAdmin(admin.ModelAdmin):
    list_display = ('name', 'width', 'height', 'crop', 'pre_cache', 'effect', 'increment_count')
    fieldsets = (
        (None, {
            'fields': ('name', 'width', 'height', 'quality')
        }),
        (_('Options'), {
            'fields': ('upscale', 'crop', 'pre_cache', 'increment_count')
        }),
        (_('Enhancements'), {
            'fields': ('effect', 'watermark',)
        }),
    )


class WatermarkAdmin(admin.ModelAdmin):
    list_display = ('name', 'opacity', 'style')


class GalleryUploadAdmin(admin.ModelAdmin):

    def has_change_permission(self, request, obj=None):
        return False  # To remove the 'Save and continue editing' button


admin.site.register(Gallery, GalleryAdmin)
admin.site.register(GalleryUpload, GalleryUploadAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(PhotoEffect, PhotoEffectAdmin)
admin.site.register(PhotoSize, PhotoSizeAdmin)
admin.site.register(Watermark, WatermarkAdmin)
