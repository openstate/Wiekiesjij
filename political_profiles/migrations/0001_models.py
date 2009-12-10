
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
            ('gender', orm['political_profiles.ChanceryProfile:gender']),
            ('telephone', orm['political_profiles.ChanceryProfile:telephone']),
            ('workingdays', orm['political_profiles.ChanceryProfile:workingdays']),
            ('street', orm['political_profiles.ChanceryProfile:street']),
            ('house_num', orm['political_profiles.ChanceryProfile:house_num']),
            ('postcode', orm['political_profiles.ChanceryProfile:postcode']),
            ('town', orm['political_profiles.ChanceryProfile:town']),
            ('website', orm['political_profiles.ChanceryProfile:website']),
            ('picture', orm['political_profiles.ChanceryProfile:picture']),
            ('description', orm['political_profiles.ChanceryProfile:description']),
        ))
        db.send_create_signal('political_profiles', ['ChanceryProfile'])
        
        # Adding model 'Link'
        db.create_table('political_profiles_link', (
            ('id', orm['political_profiles.Link:id']),
            ('name', orm['political_profiles.Link:name']),
            ('url', orm['political_profiles.Link:url']),
            ('description', orm['political_profiles.Link:description']),
            ('politician', orm['political_profiles.Link:politician']),
        ))
        db.send_create_signal('political_profiles', ['Link'])
        
        # Adding model 'Interest'
        db.create_table('political_profiles_interest', (
            ('id', orm['political_profiles.Interest:id']),
            ('organization', orm['political_profiles.Interest:organization']),
            ('url', orm['political_profiles.Interest:url']),
            ('description', orm['political_profiles.Interest:description']),
            ('politician', orm['political_profiles.Interest:politician']),
        ))
        db.send_create_signal('political_profiles', ['Interest'])
        
        # Adding model 'WorkExperienceSector'
        db.create_table('political_profiles_workexperiencesector', (
            ('id', orm['political_profiles.WorkExperienceSector:id']),
            ('sector', orm['political_profiles.WorkExperienceSector:sector']),
        ))
        db.send_create_signal('political_profiles', ['WorkExperienceSector'])
        
        # Adding model 'PoliticalExperienceType'
        db.create_table('political_profiles_politicalexperiencetype', (
            ('id', orm['political_profiles.PoliticalExperienceType:id']),
            ('type', orm['political_profiles.PoliticalExperienceType:type']),
        ))
        db.send_create_signal('political_profiles', ['PoliticalExperienceType'])
        
        # Adding model 'ContactProfile'
        db.create_table('political_profiles_contactprofile', (
            ('id', orm['political_profiles.ContactProfile:id']),
            ('user', orm['political_profiles.ContactProfile:user']),
            ('first_name', orm['political_profiles.ContactProfile:first_name']),
            ('middle_name', orm['political_profiles.ContactProfile:middle_name']),
            ('last_name', orm['political_profiles.ContactProfile:last_name']),
            ('gender', orm['political_profiles.ContactProfile:gender']),
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
        
        # Adding model 'PoliticalExperience'
        db.create_table('political_profiles_politicalexperience', (
            ('id', orm['political_profiles.PoliticalExperience:id']),
            ('organisation', orm['political_profiles.PoliticalExperience:organisation']),
            ('type', orm['political_profiles.PoliticalExperience:type']),
            ('position', orm['political_profiles.PoliticalExperience:position']),
            ('startdate', orm['political_profiles.PoliticalExperience:startdate']),
            ('enddate', orm['political_profiles.PoliticalExperience:enddate']),
            ('description', orm['political_profiles.PoliticalExperience:description']),
            ('politician', orm['political_profiles.PoliticalExperience:politician']),
            ('tags', orm['political_profiles.PoliticalExperience:tags']),
        ))
        db.send_create_signal('political_profiles', ['PoliticalExperience'])
        
        # Adding model 'EducationLevel'
        db.create_table('political_profiles_educationlevel', (
            ('id', orm['political_profiles.EducationLevel:id']),
            ('level', orm['political_profiles.EducationLevel:level']),
        ))
        db.send_create_signal('political_profiles', ['EducationLevel'])
        
        # Adding model 'Appearence'
        db.create_table('political_profiles_appearence', (
            ('id', orm['political_profiles.Appearence:id']),
            ('name', orm['political_profiles.Appearence:name']),
            ('location', orm['political_profiles.Appearence:location']),
            ('url', orm['political_profiles.Appearence:url']),
            ('description', orm['political_profiles.Appearence:description']),
            ('datetime', orm['political_profiles.Appearence:datetime']),
            ('politician', orm['political_profiles.Appearence:politician']),
        ))
        db.send_create_signal('political_profiles', ['Appearence'])
        
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
            ('picture', orm['political_profiles.PoliticianProfile:picture']),
            ('movie', orm['political_profiles.PoliticianProfile:movie']),
            ('introduction', orm['political_profiles.PoliticianProfile:introduction']),
            ('motivation', orm['political_profiles.PoliticianProfile:motivation']),
        ))
        db.send_create_signal('political_profiles', ['PoliticianProfile'])
        
        # Adding model 'Education'
        db.create_table('political_profiles_education', (
            ('id', orm['political_profiles.Education:id']),
            ('institute', orm['political_profiles.Education:institute']),
            ('level', orm['political_profiles.Education:level']),
            ('field', orm['political_profiles.Education:field']),
            ('startdate', orm['political_profiles.Education:startdate']),
            ('enddate', orm['political_profiles.Education:enddate']),
            ('description', orm['political_profiles.Education:description']),
            ('politician', orm['political_profiles.Education:politician']),
        ))
        db.send_create_signal('political_profiles', ['Education'])
        
        # Adding model 'WorkExperience'
        db.create_table('political_profiles_workexperience', (
            ('id', orm['political_profiles.WorkExperience:id']),
            ('company_name', orm['political_profiles.WorkExperience:company_name']),
            ('sector', orm['political_profiles.WorkExperience:sector']),
            ('position', orm['political_profiles.WorkExperience:position']),
            ('startdate', orm['political_profiles.WorkExperience:startdate']),
            ('enddate', orm['political_profiles.WorkExperience:enddate']),
            ('current', orm['political_profiles.WorkExperience:current']),
            ('description', orm['political_profiles.WorkExperience:description']),
            ('politician', orm['political_profiles.WorkExperience:politician']),
        ))
        db.send_create_signal('political_profiles', ['WorkExperience'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VisitorProfile'
        db.delete_table('political_profiles_visitorprofile')
        
        # Deleting model 'ChanceryProfile'
        db.delete_table('political_profiles_chanceryprofile')
        
        # Deleting model 'Link'
        db.delete_table('political_profiles_link')
        
        # Deleting model 'Interest'
        db.delete_table('political_profiles_interest')
        
        # Deleting model 'WorkExperienceSector'
        db.delete_table('political_profiles_workexperiencesector')
        
        # Deleting model 'PoliticalExperienceType'
        db.delete_table('political_profiles_politicalexperiencetype')
        
        # Deleting model 'ContactProfile'
        db.delete_table('political_profiles_contactprofile')
        
        # Deleting model 'PoliticalExperience'
        db.delete_table('political_profiles_politicalexperience')
        
        # Deleting model 'EducationLevel'
        db.delete_table('political_profiles_educationlevel')
        
        # Deleting model 'Appearence'
        db.delete_table('political_profiles_appearence')
        
        # Deleting model 'PoliticianProfile'
        db.delete_table('political_profiles_politicianprofile')
        
        # Deleting model 'Education'
        db.delete_table('political_profiles_education')
        
        # Deleting model 'WorkExperience'
        db.delete_table('political_profiles_workexperience')
        
    
    
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
        'political_profiles.appearence': {
            'datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.chanceryprofile': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
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
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'height': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contactprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'width': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'null': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.education': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'institute': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'level': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.EducationLevel']"}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        'political_profiles.educationlevel': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.interest': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organization': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.link': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.politicalexperience': {
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'organisation': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'startdate': ('django.db.models.fields.DateField', [], {}),
            'tags': ('tagging.fields.TagField', [], {'default': "''"}),
            'type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticalExperienceType']"})
        },
        'political_profiles.politicalexperiencetype': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'political_profiles.politicianprofile': {
            'dateofbirth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '25'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'introduction': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'motivation': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'movie': ('django.db.models.fields.URLField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'politicianprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.visitorprofile': {
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'visitorprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.workexperience': {
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'current': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '2550'}),
            'enddate': ('django.db.models.fields.DateField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'position': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'sector': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['political_profiles.WorkExperienceSector']"}),
            'startdate': ('django.db.models.fields.DateField', [], {})
        },
        'political_profiles.workexperiencesector': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sector': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['political_profiles']
