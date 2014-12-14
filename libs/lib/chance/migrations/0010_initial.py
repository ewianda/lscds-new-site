# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Event'
        db.create_table(u'chance_event', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('starts', self.gf('django.db.models.fields.DateTimeField')()),
            ('ends', self.gf('django.db.models.fields.DateTimeField')()),
            ('registration_limit', self.gf('django.db.models.fields.PositiveSmallIntegerField')(default=0, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=16, null=True, blank=True)),
        ))
        db.send_create_signal(u'chance', ['Event'])

        # Adding model 'EventFee'
        db.create_table(u'chance_eventfee', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='fee_options', to=orm['chance.Event'])),
            ('available', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('amount', self.gf('django.db.models.fields.DecimalField')(max_digits=65, decimal_places=2)),
        ))
        db.send_create_signal(u'chance', ['EventFee'])

        # Adding model 'EventChoice'
        db.create_table(u'chance_eventchoice', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='choices', to=orm['chance.Event'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('label', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('required', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('allow_multiple', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chance', ['EventChoice'])

        # Adding unique constraint on 'EventChoice', fields ['name', 'event']
        db.create_unique(u'chance_eventchoice', ['name', 'event_id'])

        # Adding model 'EventChoiceOption'
        db.create_table(u'chance_eventchoiceoption', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('choice', self.gf('django.db.models.fields.related.ForeignKey')(related_name='options', to=orm['chance.EventChoice'])),
            ('order', self.gf('django.db.models.fields.PositiveIntegerField')(default=0)),
            ('display', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal(u'chance', ['EventChoiceOption'])

        # Adding model 'Registration'
        db.create_table(u'chance_registration', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='registrations', to=orm['chance.Event'])),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['lscds_user.LscdsUser'])),
            ('attendee_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('attendee_email', self.gf('django.db.models.fields.EmailField')(max_length=75)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True)),
            ('fee_option', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chance.EventFee'], null=True, blank=True)),
            ('paid', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chance', ['Registration'])

        # Adding model 'EventChoiceSelection'
        db.create_table(u'chance_eventchoiceselection', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('registration', self.gf('django.db.models.fields.related.ForeignKey')(related_name='selections', to=orm['chance.Registration'])),
            ('option', self.gf('django.db.models.fields.related.ForeignKey')(related_name='+', to=orm['chance.EventChoiceOption'])),
        ))
        db.send_create_signal(u'chance', ['EventChoiceSelection'])

        # Adding model 'Talk'
        db.create_table(u'chance_talk', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['chance.Event'])),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=255, db_index=True)),
            ('presenter', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('description', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('accepted', self.gf('django.db.models.fields.NullBooleanField')(default=None, null=True, blank=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lscds_user.LscdsUser'], null=True, blank=True)),
        ))
        db.send_create_signal(u'chance', ['Talk'])

        # Adding model 'Transaction'
        db.create_table(u'chance_transaction', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('owner', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['lscds_user.LscdsUser'])),
            ('amount_paid', self.gf('django.db.models.fields.DecimalField')(default='0.00', max_digits=8, decimal_places=2)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('closed', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'chance', ['Transaction'])

        # Adding M2M table for field registrations on 'Transaction'
        m2m_table_name = db.shorten_name(u'chance_transaction_registrations')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('transaction', models.ForeignKey(orm[u'chance.transaction'], null=False)),
            ('registration', models.ForeignKey(orm[u'chance.registration'], null=False))
        ))
        db.create_unique(m2m_table_name, ['transaction_id', 'registration_id'])

        # Adding model 'Track'
        db.create_table(u'chance_track', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('event', self.gf('django.db.models.fields.related.ForeignKey')(related_name='tracks', to=orm['chance.Event'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64)),
            ('location', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
        ))
        db.send_create_signal(u'chance', ['Track'])

        # Adding model 'ScheduleItem'
        db.create_table(u'chance_scheduleitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('track', self.gf('django.db.models.fields.related.ForeignKey')(related_name='items', to=orm['chance.Track'])),
            ('talk', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='+', null=True, to=orm['chance.Talk'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('start', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('end', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'chance', ['ScheduleItem'])


    def backwards(self, orm):
        # Removing unique constraint on 'EventChoice', fields ['name', 'event']
        db.delete_unique(u'chance_eventchoice', ['name', 'event_id'])

        # Deleting model 'Event'
        db.delete_table(u'chance_event')

        # Deleting model 'EventFee'
        db.delete_table(u'chance_eventfee')

        # Deleting model 'EventChoice'
        db.delete_table(u'chance_eventchoice')

        # Deleting model 'EventChoiceOption'
        db.delete_table(u'chance_eventchoiceoption')

        # Deleting model 'Registration'
        db.delete_table(u'chance_registration')

        # Deleting model 'EventChoiceSelection'
        db.delete_table(u'chance_eventchoiceselection')

        # Deleting model 'Talk'
        db.delete_table(u'chance_talk')

        # Deleting model 'Transaction'
        db.delete_table(u'chance_transaction')

        # Removing M2M table for field registrations on 'Transaction'
        db.delete_table(db.shorten_name(u'chance_transaction_registrations'))

        # Deleting model 'Track'
        db.delete_table(u'chance_track')

        # Deleting model 'ScheduleItem'
        db.delete_table(u'chance_scheduleitem')


    models = {
        u'chance.event': {
            'Meta': {'object_name': 'Event'},
            'ends': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registration_limit': ('django.db.models.fields.PositiveSmallIntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'starts': ('django.db.models.fields.DateTimeField', [], {})
        },
        u'chance.eventchoice': {
            'Meta': {'ordering': "('order',)", 'unique_together': "(('name', 'event'),)", 'object_name': 'EventChoice'},
            'allow_multiple': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'choices'", 'to': u"orm['chance.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'label': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'required': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'chance.eventchoiceoption': {
            'Meta': {'ordering': "('order',)", 'object_name': 'EventChoiceOption'},
            'choice': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'options'", 'to': u"orm['chance.EventChoice']"}),
            'display': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'order': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        u'chance.eventchoiceselection': {
            'Meta': {'object_name': 'EventChoiceSelection'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'option': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': u"orm['chance.EventChoiceOption']"}),
            'registration': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'selections'", 'to': u"orm['chance.Registration']"})
        },
        u'chance.eventfee': {
            'Meta': {'object_name': 'EventFee'},
            'amount': ('django.db.models.fields.DecimalField', [], {'max_digits': '65', 'decimal_places': '2'}),
            'available': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'fee_options'", 'to': u"orm['chance.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'chance.registration': {
            'Meta': {'ordering': "('created',)", 'object_name': 'Registration'},
            'attendee_email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'attendee_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'registrations'", 'to': u"orm['chance.Event']"}),
            'fee_option': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chance.EventFee']", 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['lscds_user.LscdsUser']"}),
            'paid': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'chance.scheduleitem': {
            'Meta': {'ordering': "('start', 'track')", 'object_name': 'ScheduleItem'},
            'end': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'start': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'talk': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['chance.Talk']"}),
            'track': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'items'", 'to': u"orm['chance.Track']"})
        },
        u'chance.talk': {
            'Meta': {'ordering': "('event', 'title')", 'object_name': 'Talk'},
            'accepted': ('django.db.models.fields.NullBooleanField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'event': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['chance.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lscds_user.LscdsUser']", 'null': 'True', 'blank': 'True'}),
            'presenter': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255', 'db_index': 'True'})
        },
        u'chance.track': {
            'Meta': {'object_name': 'Track'},
            'event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tracks'", 'to': u"orm['chance.Event']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'chance.transaction': {
            'Meta': {'object_name': 'Transaction'},
            'amount_paid': ('django.db.models.fields.DecimalField', [], {'default': "'0.00'", 'max_digits': '8', 'decimal_places': '2'}),
            'closed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'owner': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'+'", 'null': 'True', 'to': u"orm['lscds_user.LscdsUser']"}),
            'registrations': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'+'", 'symmetrical': 'False', 'to': u"orm['chance.Registration']"})
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

    complete_apps = ['chance']