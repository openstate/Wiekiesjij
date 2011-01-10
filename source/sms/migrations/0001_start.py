
from south.db import db
from django.db import models
from sms.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Sms'
        db.create_table('sms_sms', (
            ('id', orm['sms.Sms:id']),
            ('originator', orm['sms.Sms:originator']),
            ('sent_time', orm['sms.Sms:sent_time']),
            ('recipients', orm['sms.Sms:recipients']),
            ('numbers_sent_to', orm['sms.Sms:numbers_sent_to']),
            ('sent', orm['sms.Sms:sent']),
            ('success', orm['sms.Sms:success']),
            ('resultmessage', orm['sms.Sms:resultmessage']),
            ('resultcode', orm['sms.Sms:resultcode']),
            ('error', orm['sms.Sms:error']),
            ('message', orm['sms.Sms:message']),
            ('deliverydate', orm['sms.Sms:deliverydate']),
            ('scheduling_description', orm['sms.Sms:scheduling_description']),
        ))
        db.send_create_signal('sms', ['Sms'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Sms'
        db.delete_table('sms_sms')
        
    
    
    models = {
        'sms.sms': {
            'deliverydate': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'error': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '160'}),
            'numbers_sent_to': ('django.db.models.fields.TextField', [], {}),
            'originator': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'recipients': ('django.db.models.fields.TextField', [], {}),
            'resultcode': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'resultmessage': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'scheduling_description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'sent_time': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'success': ('django.db.models.fields.TextField', [], {})
        }
    }
    
    complete_apps = ['sms']
