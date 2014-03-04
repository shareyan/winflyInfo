# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'downloadCount'
        db.create_table(u'info_downloadcount', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'info', ['downloadCount'])


    def backwards(self, orm):
        # Deleting model 'downloadCount'
        db.delete_table(u'info_downloadcount')


    models = {
        u'info.downloadcount': {
            'Meta': {'object_name': 'downloadCount'},
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['info']