
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
            ('email', orm['political_profiles.ChanceryProfile:email']),
            ('telephone', orm['political_profiles.ChanceryProfile:telephone']),
            ('workingdays', orm['political_profiles.ChanceryProfile:workingdays']),
            ('street', orm['political_profiles.ChanceryProfile:street']),
            ('house_num', orm['political_profiles.ChanceryProfile:house_num']),
            ('postcode', orm['political_profiles.ChanceryProfile:postcode']),
            ('town', orm['political_profiles.ChanceryProfile:town']),
            ('website', orm['political_profiles.ChanceryProfile:website']),
            ('picture', orm['political_profiles.ChanceryProfile:picture']),
            ('width', orm['political_profiles.ChanceryProfile:width']),
            ('height', orm['political_profiles.ChanceryProfile:height']),
            ('description', orm['political_profiles.ChanceryProfile:description']),
        ))
        db.send_create_signal('political_profiles', ['ChanceryProfile'])
        
        # Adding model 'PoliticianProfile'
        db.create_table('political_profiles_politicianprofile', (
            ('id', orm['political_profiles.PoliticianProfile:id']),
            ('user', orm['political_profiles.PoliticianProfile:user']),
            ('first_name', orm['political_profiles.PoliticianProfile:first_name']),
            ('middle_name', orm['political_profiles.PoliticianProfile:middle_name']),
            ('last_name', orm['political_profiles.PoliticianProfile:last_name']),
            ('initials', orm['political_profiles.PoliticianProfile:initials']),
            ('gender', orm['political_profiles.PoliticianProfile:gender']),
            ('dateofbirth', orm['political_profiles.PoliticianProfile:dateofbirth']),
            ('email', orm['political_profiles.PoliticianProfile:email']),
            ('picture', orm['political_profiles.PoliticianProfile:picture']),
            ('width', orm['political_profiles.PoliticianProfile:width']),
            ('height', orm['political_profiles.PoliticianProfile:height']),
            ('movie', orm['political_profiles.PoliticianProfile:movie']),
            ('introduction', orm['political_profiles.PoliticianProfile:introduction']),
            ('motivation', orm['political_profiles.PoliticianProfile:motivation']),
        ))
        db.send_create_signal('political_profiles', ['PoliticianProfile'])
        
        # Adding model 'ContactProfile'
        db.create_table('political_profiles_contactprofile', (
            ('id', orm['political_profiles.ContactProfile:id']),
            ('user', orm['political_profiles.ContactProfile:user']),
            ('first_name', orm['political_profiles.ContactProfile:first_name']),
            ('middle_name', orm['political_profiles.ContactProfile:middle_name']),
            ('last_name', orm['political_profiles.ContactProfile:last_name']),
            ('email', orm['political_profiles.ContactProfile:email']),
            ('telephone', orm['political_profiles.ContactProfile:telephone']),
            ('workingdays', orm['political_profiles.ContactProfile:workingdays']),
            ('street', orm['political_profiles.ContactProfile:street']),
            ('house_num', orm['political_profiles.ContactProfile:house_num']),
            ('postcode', orm['political_profiles.ContactProfile:postcode']),
            ('town', orm['political_profiles.ContactProfile:town']),
            ('website', orm['political_profiles.ContactProfile:website']),
            ('picture', orm['political_profiles.ContactProfile:picture']),
            ('width', orm['political_profiles.ContactProfile:width']),
            ('height', orm['political_profiles.ContactProfile:height']),
            ('description', orm['political_profiles.ContactProfile:description']),
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
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'chanceryprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.contactprofile': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contactprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.politicianprofile': {
            'dateofbirth': ('django.db.models.fields.DateField', [], {}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'motivation': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'movie': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'editable': 'False', 'default': '0', 'null': 'True'}),
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
