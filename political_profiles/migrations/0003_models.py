
from south.db import db
from django.db import models
from political_profiles.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'PoliticianProfile.diet'
        db.add_column('political_profiles_politicianprofile', 'diet', orm['political_profiles.politicianprofile:diet'])
        
        # Adding field 'PoliticianProfile.hobby'
        db.add_column('political_profiles_politicianprofile', 'hobby', orm['political_profiles.politicianprofile:hobby'])
        
        # Adding field 'PoliticianProfile.fav_pet'
        db.add_column('political_profiles_politicianprofile', 'fav_pet', orm['political_profiles.politicianprofile:fav_pet'])
        
        # Adding field 'PoliticianProfile.marital_status'
        db.add_column('political_profiles_politicianprofile', 'marital_status', orm['political_profiles.politicianprofile:marital_status'])
        
        # Adding field 'PoliticianProfile.church'
        db.add_column('political_profiles_politicianprofile', 'church', orm['political_profiles.politicianprofile:church'])
        
        # Adding field 'PoliticianProfile.transport'
        db.add_column('political_profiles_politicianprofile', 'transport', orm['political_profiles.politicianprofile:transport'])
        
        # Adding field 'PoliticianProfile.fav_club'
        db.add_column('political_profiles_politicianprofile', 'fav_club', orm['political_profiles.politicianprofile:fav_club'])
        
        # Adding field 'PoliticianProfile.fav_news'
        db.add_column('political_profiles_politicianprofile', 'fav_news', orm['political_profiles.politicianprofile:fav_news'])
        
        # Adding field 'PoliticianProfile.charity'
        db.add_column('political_profiles_politicianprofile', 'charity', orm['political_profiles.politicianprofile:charity'])
        
        # Adding field 'PoliticianProfile.life_stance'
        db.add_column('political_profiles_politicianprofile', 'life_stance', orm['political_profiles.politicianprofile:life_stance'])
        
        # Adding field 'PoliticianProfile.fav_media'
        db.add_column('political_profiles_politicianprofile', 'fav_media', orm['political_profiles.politicianprofile:fav_media'])
        
        # Adding field 'PoliticianProfile.fav_sport'
        db.add_column('political_profiles_politicianprofile', 'fav_sport', orm['political_profiles.politicianprofile:fav_sport'])
        
        # Adding field 'PoliticianProfile.num_children'
        db.add_column('political_profiles_politicianprofile', 'num_children', orm['political_profiles.politicianprofile:num_children'])
        
        # Adding field 'PoliticianProfile.smoker'
        db.add_column('political_profiles_politicianprofile', 'smoker', orm['political_profiles.politicianprofile:smoker'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'PoliticianProfile.diet'
        db.delete_column('political_profiles_politicianprofile', 'diet')
        
        # Deleting field 'PoliticianProfile.hobby'
        db.delete_column('political_profiles_politicianprofile', 'hobby')
        
        # Deleting field 'PoliticianProfile.fav_pet'
        db.delete_column('political_profiles_politicianprofile', 'fav_pet')
        
        # Deleting field 'PoliticianProfile.marital_status'
        db.delete_column('political_profiles_politicianprofile', 'marital_status')
        
        # Deleting field 'PoliticianProfile.church'
        db.delete_column('political_profiles_politicianprofile', 'church')
        
        # Deleting field 'PoliticianProfile.transport'
        db.delete_column('political_profiles_politicianprofile', 'transport')
        
        # Deleting field 'PoliticianProfile.fav_club'
        db.delete_column('political_profiles_politicianprofile', 'fav_club')
        
        # Deleting field 'PoliticianProfile.fav_news'
        db.delete_column('political_profiles_politicianprofile', 'fav_news')
        
        # Deleting field 'PoliticianProfile.charity'
        db.delete_column('political_profiles_politicianprofile', 'charity')
        
        # Deleting field 'PoliticianProfile.life_stance'
        db.delete_column('political_profiles_politicianprofile', 'life_stance')
        
        # Deleting field 'PoliticianProfile.fav_media'
        db.delete_column('political_profiles_politicianprofile', 'fav_media')
        
        # Deleting field 'PoliticianProfile.fav_sport'
        db.delete_column('political_profiles_politicianprofile', 'fav_sport')
        
        # Deleting field 'PoliticianProfile.num_children'
        db.delete_column('political_profiles_politicianprofile', 'num_children')
        
        # Deleting field 'PoliticianProfile.smoker'
        db.delete_column('political_profiles_politicianprofile', 'smoker')
        
    
    
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
        'political_profiles.appearance': {
            'datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'appearances'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.chanceryprofile': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '25'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'chanceryprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.connection': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'connections'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.ConnectionType']", 'null': 'True', 'blank': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'political_profiles.connectiontype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.contactprofile': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '25'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contactprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.education': {
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.EducationLevel']", 'null': 'True', 'blank': 'True'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'education'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'startdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'political_profiles.educationlevel': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.interest': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'interests'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'political_profiles.link': {
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'links'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'political_profiles.politicalexperience': {
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'political'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'startdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticalExperienceType']", 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.politicalexperiencetype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.politicianprofile': {
            'charity': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'church': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'dateofbirth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_club': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_media': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_news': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_pet': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_sport': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '25'}),
            'hobby': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'life_stance': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'motivation': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_children': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'politicianprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.visitorprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'visitorprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.workexperience': {
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'enddate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'work'", 'to': "orm['political_profiles.PoliticianProfile']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.WorkExperienceSector']", 'null': 'True', 'blank': 'True'}),
            'startdate': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'})
        },
        'political_profiles.workexperiencesector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['political_profiles']
