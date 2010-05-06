# -*- coding: utf-8 -*-

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
            ('terms_and_conditions', orm['political_profiles.VisitorProfile:terms_and_conditions']),
            ('phone', orm['political_profiles.VisitorProfile:phone']),
            ('send_text', orm['political_profiles.VisitorProfile:send_text']),
        ))
        db.send_create_signal('political_profiles', ['VisitorProfile'])
        
        # Adding model 'ChanceryProfile'
        db.create_table('political_profiles_chanceryprofile', (
            ('id', orm['political_profiles.ChanceryProfile:id']),
            ('user', orm['political_profiles.ChanceryProfile:user']),
            ('first_name', orm['political_profiles.ChanceryProfile:first_name']),
            ('middle_name', orm['political_profiles.ChanceryProfile:middle_name']),
            ('last_name', orm['political_profiles.ChanceryProfile:last_name']),
            ('terms_and_conditions', orm['political_profiles.ChanceryProfile:terms_and_conditions']),
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
        
        # Adding model 'ConnectionType'
        db.create_table('political_profiles_connectiontype', (
            ('id', orm['political_profiles.ConnectionType:id']),
            ('type', orm['political_profiles.ConnectionType:type']),
        ))
        db.send_create_signal('political_profiles', ['ConnectionType'])
        
        # Adding model 'Connection'
        db.create_table('political_profiles_connection', (
            ('id', orm['political_profiles.Connection:id']),
            ('type', orm['political_profiles.Connection:type']),
            ('url', orm['political_profiles.Connection:url']),
            ('description', orm['political_profiles.Connection:description']),
            ('politician', orm['political_profiles.Connection:politician']),
        ))
        db.send_create_signal('political_profiles', ['Connection'])
        
        # Adding model 'Interest'
        db.create_table('political_profiles_interest', (
            ('id', orm['political_profiles.Interest:id']),
            ('organisation', orm['political_profiles.Interest:organisation']),
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
        
        # Adding model 'Appearance'
        db.create_table('political_profiles_appearance', (
            ('id', orm['political_profiles.Appearance:id']),
            ('name', orm['political_profiles.Appearance:name']),
            ('location', orm['political_profiles.Appearance:location']),
            ('url', orm['political_profiles.Appearance:url']),
            ('description', orm['political_profiles.Appearance:description']),
            ('datetime', orm['political_profiles.Appearance:datetime']),
            ('politician', orm['political_profiles.Appearance:politician']),
        ))
        db.send_create_signal('political_profiles', ['Appearance'])
        
        # Adding model 'UserStatistics'
        db.create_table('political_profiles_userstatistics', (
            ('id', orm['political_profiles.UserStatistics:id']),
            ('user', orm['political_profiles.UserStatistics:user']),
            ('profile_hits', orm['political_profiles.UserStatistics:profile_hits']),
            ('profile_hits_up', orm['political_profiles.UserStatistics:profile_hits_up']),
        ))
        db.send_create_signal('political_profiles', ['UserStatistics'])
        
        # Adding model 'ContactProfile'
        db.create_table('political_profiles_contactprofile', (
            ('id', orm['political_profiles.ContactProfile:id']),
            ('user', orm['political_profiles.ContactProfile:user']),
            ('first_name', orm['political_profiles.ContactProfile:first_name']),
            ('middle_name', orm['political_profiles.ContactProfile:middle_name']),
            ('last_name', orm['political_profiles.ContactProfile:last_name']),
            ('terms_and_conditions', orm['political_profiles.ContactProfile:terms_and_conditions']),
            ('gender', orm['political_profiles.ContactProfile:gender']),
            ('telephone', orm['political_profiles.ContactProfile:telephone']),
            ('workingdays', orm['political_profiles.ContactProfile:workingdays']),
            ('street', orm['political_profiles.ContactProfile:street']),
            ('house_num', orm['political_profiles.ContactProfile:house_num']),
            ('postcode', orm['political_profiles.ContactProfile:postcode']),
            ('town', orm['political_profiles.ContactProfile:town']),
            ('website', orm['political_profiles.ContactProfile:website']),
            ('picture', orm['political_profiles.ContactProfile:picture']),
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
        ))
        db.send_create_signal('political_profiles', ['PoliticalExperience'])
        
        # Adding model 'EducationLevel'
        db.create_table('political_profiles_educationlevel', (
            ('id', orm['political_profiles.EducationLevel:id']),
            ('level', orm['political_profiles.EducationLevel:level']),
        ))
        db.send_create_signal('political_profiles', ['EducationLevel'])
        
        # Adding model 'PoliticianProfile'
        db.create_table('political_profiles_politicianprofile', (
            ('id', orm['political_profiles.PoliticianProfile:id']),
            ('user', orm['political_profiles.PoliticianProfile:user']),
            ('first_name', orm['political_profiles.PoliticianProfile:first_name']),
            ('middle_name', orm['political_profiles.PoliticianProfile:middle_name']),
            ('last_name', orm['political_profiles.PoliticianProfile:last_name']),
            ('terms_and_conditions', orm['political_profiles.PoliticianProfile:terms_and_conditions']),
            ('initials', orm['political_profiles.PoliticianProfile:initials']),
            ('gender', orm['political_profiles.PoliticianProfile:gender']),
            ('dateofbirth', orm['political_profiles.PoliticianProfile:dateofbirth']),
            ('age', orm['political_profiles.PoliticianProfile:age']),
            ('picture', orm['political_profiles.PoliticianProfile:picture']),
            ('movie', orm['political_profiles.PoliticianProfile:movie']),
            ('introduction', orm['political_profiles.PoliticianProfile:introduction']),
            ('marital_status', orm['political_profiles.PoliticianProfile:marital_status']),
            ('num_children', orm['political_profiles.PoliticianProfile:num_children']),
            ('religion', orm['political_profiles.PoliticianProfile:religion']),
            ('religious_group', orm['political_profiles.PoliticianProfile:religious_group']),
            ('smoker', orm['political_profiles.PoliticianProfile:smoker']),
            ('diet', orm['political_profiles.PoliticianProfile:diet']),
            ('fav_news', orm['political_profiles.PoliticianProfile:fav_news']),
            ('transport', orm['political_profiles.PoliticianProfile:transport']),
            ('charity', orm['political_profiles.PoliticianProfile:charity']),
            ('fav_media', orm['political_profiles.PoliticianProfile:fav_media']),
            ('fav_sport', orm['political_profiles.PoliticianProfile:fav_sport']),
            ('hobby', orm['political_profiles.PoliticianProfile:hobby']),
            ('fav_club', orm['political_profiles.PoliticianProfile:fav_club']),
            ('fav_pet', orm['political_profiles.PoliticianProfile:fav_pet']),
            ('political_experience_days', orm['political_profiles.PoliticianProfile:political_experience_days']),
            ('work_experience_days', orm['political_profiles.PoliticianProfile:work_experience_days']),
            ('hns_dev', orm['political_profiles.PoliticianProfile:hns_dev']),
            ('science', orm['political_profiles.PoliticianProfile:science']),
        ))
        db.send_create_signal('political_profiles', ['PoliticianProfile'])
        
        # Adding model 'PoliticalGoal'
        db.create_table('political_profiles_politicalgoal', (
            ('id', orm['political_profiles.PoliticalGoal:id']),
            ('goal', orm['political_profiles.PoliticalGoal:goal']),
            ('politician', orm['political_profiles.PoliticalGoal:politician']),
        ))
        db.send_create_signal('political_profiles', ['PoliticalGoal'])
        
        # Adding model 'GoalRanking'
        db.create_table('political_profiles_goalranking', (
            ('id', orm['political_profiles.GoalRanking:id']),
            ('ranking', orm['political_profiles.GoalRanking:ranking']),
            ('goal', orm['political_profiles.GoalRanking:goal']),
            ('user', orm['political_profiles.GoalRanking:user']),
        ))
        db.send_create_signal('political_profiles', ['GoalRanking'])
        
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
            ('description', orm['political_profiles.WorkExperience:description']),
            ('politician', orm['political_profiles.WorkExperience:politician']),
        ))
        db.send_create_signal('political_profiles', ['WorkExperience'])
        
        # Adding ManyToManyField 'VisitorProfile.favorites'
        db.create_table('political_profiles_visitorprofile_favorites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('visitorprofile', models.ForeignKey(orm.VisitorProfile, null=False)),
            ('politicianprofile', models.ForeignKey(orm.PoliticianProfile, null=False))
        ))
        
        # Creating unique_together for [goal, user] on GoalRanking.
        db.create_unique('political_profiles_goalranking', ['goal_id', 'user_id'])
        
    
    
    def backwards(self, orm):
        
        # Deleting unique_together for [goal, user] on GoalRanking.
        db.delete_unique('political_profiles_goalranking', ['goal_id', 'user_id'])
        
        # Deleting model 'VisitorProfile'
        db.delete_table('political_profiles_visitorprofile')
        
        # Deleting model 'ChanceryProfile'
        db.delete_table('political_profiles_chanceryprofile')
        
        # Deleting model 'Link'
        db.delete_table('political_profiles_link')
        
        # Deleting model 'ConnectionType'
        db.delete_table('political_profiles_connectiontype')
        
        # Deleting model 'Connection'
        db.delete_table('political_profiles_connection')
        
        # Deleting model 'Interest'
        db.delete_table('political_profiles_interest')
        
        # Deleting model 'WorkExperienceSector'
        db.delete_table('political_profiles_workexperiencesector')
        
        # Deleting model 'PoliticalExperienceType'
        db.delete_table('political_profiles_politicalexperiencetype')
        
        # Deleting model 'Appearance'
        db.delete_table('political_profiles_appearance')
        
        # Deleting model 'UserStatistics'
        db.delete_table('political_profiles_userstatistics')
        
        # Deleting model 'ContactProfile'
        db.delete_table('political_profiles_contactprofile')
        
        # Deleting model 'PoliticalExperience'
        db.delete_table('political_profiles_politicalexperience')
        
        # Deleting model 'EducationLevel'
        db.delete_table('political_profiles_educationlevel')
        
        # Deleting model 'PoliticianProfile'
        db.delete_table('political_profiles_politicianprofile')
        
        # Deleting model 'PoliticalGoal'
        db.delete_table('political_profiles_politicalgoal')
        
        # Deleting model 'GoalRanking'
        db.delete_table('political_profiles_goalranking')
        
        # Deleting model 'Education'
        db.delete_table('political_profiles_education')
        
        # Deleting model 'WorkExperience'
        db.delete_table('political_profiles_workexperience')
        
        # Dropping ManyToManyField 'VisitorProfile.favorites'
        db.delete_table('political_profiles_visitorprofile_favorites')
        
    
    
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
            'terms_and_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
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
            'terms_and_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'contactprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'workingdays': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.education': {
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
        'political_profiles.goalranking': {
            'Meta': {'unique_together': "(('goal', 'user'),)"},
            'goal': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'rankings'", 'to': "orm['political_profiles.PoliticalGoal']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ranking': ('django.db.models.fields.SmallIntegerField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
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
        'political_profiles.politicalgoal': {
            'goal': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'goals'", 'to': "orm['political_profiles.PoliticianProfile']"})
        },
        'political_profiles.politicianprofile': {
            'age': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'charity': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'dateofbirth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'diet': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_club': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fav_media': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_news': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'fav_pet': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'fav_sport': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'default': "'Male'", 'max_length': '25'}),
            'hns_dev': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'hobby': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'introduction': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'marital_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'num_children': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'political_experience_days': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'religion': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'religious_group': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'science': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'smoker': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'terms_and_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'transport': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'politicianprofile'", 'unique': 'True', 'to': "orm['auth.User']"}),
            'work_experience_days': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'political_profiles.userstatistics': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'profile_hits': ('django.db.models.fields.FloatField', [], {'default': '1'}),
            'profile_hits_up': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'stats'", 'unique': 'True', 'null': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.visitorprofile': {
            'favorites': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['political_profiles.PoliticianProfile']"}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'blank': 'True'}),
            'middle_name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'send_text': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'terms_and_conditions': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'visitorprofile'", 'unique': 'True', 'to': "orm['auth.User']"})
        },
        'political_profiles.workexperience': {
            'company_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
