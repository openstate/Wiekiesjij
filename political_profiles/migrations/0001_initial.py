
from south.db import db
from django.db import models
from political_profiles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VisitorProfile'
        db.create_table('political_profiles_visitorprofile', (
            ('id', orm['political_profiles.VisitorProfile:id']),
            ('user', orm['political_profiles.VisitorProfile:user']),
            ('first_name', orm['political_profiles.VisitorProfile:first_name']),
            ('middle_name', orm['political_profiles.VisitorProfile:middle_name']),
            ('last_name', orm['political_profiles.VisitorProfile:last_name']),
        ))
        db.send_create_signal('political_profiles', ['VisitorProfile'])
        
        # Adding model 'ChanceryProfile'
        db.create_table('political_profiles_chanceryprofile', (
            ('id', orm['political_profiles.ChanceryProfile:id']),
            ('user', orm['political_profiles.ChanceryProfile:user']),
            ('first_name', orm['political_profiles.ChanceryProfile:first_name']),
            ('middle_name', orm['political_profiles.ChanceryProfile:middle_name']),
            ('last_name', orm['political_profiles.ChanceryProfile:last_name']),
        ))
        db.send_create_signal('political_profiles', ['ChanceryProfile'])
        
        # Adding model 'PoliticianProfile'
        db.create_table('political_profiles_politicianprofile', (
            ('id', orm['political_profiles.PoliticianProfile:id']),
            ('user', orm['political_profiles.PoliticianProfile:user']),
            ('first_name', orm['political_profiles.PoliticianProfile:first_name']),
            ('middle_name', orm['political_profiles.PoliticianProfile:middle_name']),
            ('last_name', orm['political_profiles.PoliticianProfile:last_name']),
        ))
        db.send_create_signal('political_profiles', ['PoliticianProfile'])
        
        # Adding model 'ContactProfile'
        db.create_table('political_profiles_contactprofile', (
            ('id', orm['political_profiles.ContactProfile:id']),
            ('user', orm['political_profiles.ContactProfile:user']),
            ('first_name', orm['political_profiles.ContactProfile:first_name']),
            ('middle_name', orm['political_profiles.ContactProfile:middle_name']),
            ('last_name', orm['political_profiles.ContactProfile:last_name']),
        ))
        db.send_create_signal('political_profiles', ['ContactProfile'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VisitorProfile'
        db.delete_table('political_profiles_visitorprofile')
        
        # Deleting model 'ChanceryProfile'
        db.delete_table('political_profiles_chanceryprofile')
        
        # Deleting model 'PoliticianProfile'
        db.delete_table('political_profiles_politicianprofile')
        
        # Deleting model 'ContactProfile'
        db.delete_table('political_profiles_contactprofile')
        
    
    
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
        'political_profiles.chanceryprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'chanceryprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.contactprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contactprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.politicianprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'politicianprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.visitorprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'visitorprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        }
    }
    
    complete_apps = ['political_profiles']
