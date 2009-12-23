
from south.db import db
from django.db import models
from elections.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Council.description'
        # (to signature: django.db.models.fields.TextField(null=True, blank=True))
        db.alter_column('elections_council', 'description', orm['elections.council:description'])
        
        # Changing field 'Council.history'
        # (to signature: django.db.models.fields.TextField(null=True, blank=True))
        db.alter_column('elections_council', 'history', orm['elections.council:history'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Council.description'
        # (to signature: django.db.models.fields.CharField(max_length=255, null=True, blank=True))
        db.alter_column('elections_council', 'description', orm['elections.council:description'])
        
        # Changing field 'Council.history'
        # (to signature: django.db.models.fields.CharField(max_length=255, null=True, blank=True))
        db.alter_column('elections_council', 'history', orm['elections.council:history'])
        
    
    
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
        'elections.candidacy': {
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Answer']"}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elections'", 'to': "orm['auth.User']"}),
            'election_party_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'candidates'", 'to': "orm['elections.ElectionInstanceParty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.council': {
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'another_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'chanceries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'foreground_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'house_num': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '7'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'seats': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'street': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'town': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'elections.electionevent': {
            'candidate_due_period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'default_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party_due_period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'profile_due_period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_due_period': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.electioninstance': {
            'council': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instances'", 'to': "orm['elections.Council']"}),
            'election_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionEvent']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.ElectionInstanceModule']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_lists': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.Party']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']", 'null': 'True', 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wizard_start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'elections.electioninstancemodule': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'elections.electioninstanceparty': {
            'Meta': {'unique_together': "(('election_instance', 'position'),)"},
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instance_parties'", 'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instance_parties'", 'to': "orm['elections.Party']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.electioninstancequestion': {
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'elections.electioninstancequestionanswer': {
            'Meta': {'unique_together': "(('election_instance_question', 'candidate'),)"},
            'answer_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'election_instance_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstanceQuestion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'elections.party': {
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'goals': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manifesto': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'manifesto_summary': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'movie': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_seats': ('django.db.models.fields.PositiveIntegerField', [], {'null': 'True', 'blank': 'True'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slogan': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'questions.answer': {
            'frontoffice_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'frontend_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'has_no_preference': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }
    
    complete_apps = ['elections']
