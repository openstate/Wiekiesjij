
from south.db import db
from django.db import models
from invitations.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Invitation'
        db.create_table('invitations_invitation', (
            ('id', orm['invitations.Invitation:id']),
            ('user_from', orm['invitations.Invitation:user_from']),
            ('user_to', orm['invitations.Invitation:user_to']),
            ('hash', orm['invitations.Invitation:hash']),
            ('view', orm['invitations.Invitation:view']),
            ('text', orm['invitations.Invitation:text']),
            ('subject', orm['invitations.Invitation:subject']),
            ('html_template', orm['invitations.Invitation:html_template']),
            ('plain_template', orm['invitations.Invitation:plain_template']),
            ('accepted', orm['invitations.Invitation:accepted']),
            ('send_on', orm['invitations.Invitation:send_on']),
            ('created', orm['invitations.Invitation:created']),
            ('updated', orm['invitations.Invitation:updated']),
        ))
        db.send_create_signal('invitations', ['Invitation'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Invitation'
        db.delete_table('invitations_invitation')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'invitations.invitation': {
            'accepted': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'html_template': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'plain_template': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'send_on': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'text': ('django.db.models.fields.TextField', [], {}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user_from': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_from'", 'to': "orm['auth.User']"}),
            'user_to': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'invitation_to'", 'to': "orm['auth.User']"}),
            'view': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['invitations']
