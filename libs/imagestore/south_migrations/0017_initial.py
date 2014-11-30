# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table(u'imagestore_album', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'albums', null=True, to=orm['lscds_user.LscdsUser'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('brief', self.gf('django.db.models.fields.CharField')(default=u'', max_length=255, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('is_public', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('head', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'head_of', null=True, on_delete=models.SET_NULL, to=orm['imagestore.Image'])),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('imagestore', ['Album'])

        # Adding model 'Image'
        db.create_table(u'imagestore_image', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('tags', self.gf('tagging.fields.TagField')()),
            ('order', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('image', self.gf('sorl.thumbnail.fields.ImageField')(max_length=255)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'images', null=True, to=orm['lscds_user.LscdsUser'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, null=True, blank=True)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name=u'images', null=True, to=orm['imagestore.Album'])),
        ))
        db.send_create_signal('imagestore', ['Image'])

        # Adding model 'AlbumUpload'
        db.create_table(u'imagestore_albumupload', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('zip_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('album', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['imagestore.Album'], null=True, blank=True)),
            ('new_album_name', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
            ('tags', self.gf('django.db.models.fields.CharField')(max_length=255, blank=True)),
        ))
        db.send_create_signal('imagestore', ['AlbumUpload'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table(u'imagestore_album')

        # Deleting model 'Image'
        db.delete_table(u'imagestore_image')

        # Deleting model 'AlbumUpload'
        db.delete_table(u'imagestore_albumupload')


    models = {
        'imagestore.album': {
            'Meta': {'ordering': "(u'order', u'created', u'name')", 'object_name': 'Album'},
            'brief': ('django.db.models.fields.CharField', [], {'default': "u''", 'max_length': '255', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'head': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'head_of'", 'null': 'True', 'on_delete': 'models.SET_NULL', 'to': "orm['imagestore.Image']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_public': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'albums'", 'null': 'True', 'to': u"orm['lscds_user.LscdsUser']"})
        },
        'imagestore.albumupload': {
            'Meta': {'object_name': 'AlbumUpload'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['imagestore.Album']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'new_album_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'tags': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'zip_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        },
        'imagestore.image': {
            'Meta': {'ordering': "(u'order', u'id')", 'object_name': 'Image'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'images'", 'null': 'True', 'to': "orm['imagestore.Album']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('sorl.thumbnail.fields.ImageField', [], {'max_length': '255'}),
            'order': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tags': ('tagging.fields.TagField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "u'images'", 'null': 'True', 'to': u"orm['lscds_user.LscdsUser']"})
        },
        u'lscds_user.lscdsuser': {
            'Meta': {'object_name': 'LscdsUser'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '255'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        }
    }

    complete_apps = ['imagestore']