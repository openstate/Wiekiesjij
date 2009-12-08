
from south.db import db
from django.db import models
from elections.models import *

class Migration:
    def forwards(self, orm):
        
        # Adding model 'ElectionInstanceQuestion'
        db.create_table('elections_electioninstancequestion', (
            ('id', orm['elections.ElectionInstanceQuestion:id']),
            ('election_instance', orm['elections.ElectionInstanceQuestion:election_instance']),
            ('question', orm['elections.ElectionInstanceQuestion:question']),
            ('locked', orm['elections.ElectionInstanceQuestion:locked']),
        ))
        db.send_create_signal('elections', ['ElectionInstanceQuestion'])
        
        # Adding model 'Council'
        db.create_table('elections_council', (
            ('id', orm['elections.Council:id']),
            ('name', orm['elections.Council:name']),
            ('region', orm['elections.Council:region']),
            ('level', orm['elections.Council:level']),
            ('abbreviation', orm['elections.Council:abbreviation']),
            ('email', orm['elections.Council:email']),
            ('street', orm['elections.Council:street']),
            ('house_num', orm['elections.Council:house_num']),
            ('postcode', orm['elections.Council:postcode']),
            ('town', orm['elections.Council:town']),
            ('seats', orm['elections.Council:seats']),
            ('website', orm['elections.Council:website']),
            ('picture', orm['elections.Council:picture']),
            ('desciption', orm['elections.Council:desciption']),
            ('history', orm['elections.Council:history']),
            ('background_color', orm['elections.Council:background_color']),
            ('foreground_color', orm['elections.Council:foreground_color']),
            ('another_color', orm['elections.Council:another_color']),
        ))
        db.send_create_signal('elections', ['Council'])
        
        # Adding model 'ElectionEvent'
        db.create_table('elections_electionevent', (
            ('id', orm['elections.ElectionEvent:id']),
            ('name', orm['elections.ElectionEvent:name']),
            ('parent_region', orm['elections.ElectionEvent:parent_region']),
            ('level', orm['elections.ElectionEvent:level']),
            ('desciption', orm['elections.ElectionEvent:desciption']),
            ('question_due_period', orm['elections.ElectionEvent:question_due_period']),
            ('profile_due_period', orm['elections.ElectionEvent:profile_due_period']),
            ('candidate_due_period', orm['elections.ElectionEvent:candidate_due_period']),
            ('party_due_period', orm['elections.ElectionEvent:party_due_period']),
        ))
        db.send_create_signal('elections', ['ElectionEvent'])
        
        # Adding model 'Candidacy'
        db.create_table('elections_candidacy', (
            ('id', orm['elections.Candidacy:id']),
            ('election_party_instance', orm['elections.Candidacy:election_party_instance']),
            ('candidate', orm['elections.Candidacy:candidate']),
            ('position', orm['elections.Candidacy:position']),
        ))
        db.send_create_signal('elections', ['Candidacy'])
        
        # Adding model 'ElectionInstanceParty'
        db.create_table('elections_electioninstanceparty', (
            ('id', orm['elections.ElectionInstanceParty:id']),
            ('election_instance', orm['elections.ElectionInstanceParty:election_instance']),
            ('party', orm['elections.ElectionInstanceParty:party']),
            ('position', orm['elections.ElectionInstanceParty:position']),
            ('list_length', orm['elections.ElectionInstanceParty:list_length']),
        ))
        db.send_create_signal('elections', ['ElectionInstanceParty'])
        
        # Adding model 'ElectionInstanceModule'
        db.create_table('elections_electioninstancemodule', (
            ('id', orm['elections.ElectionInstanceModule:id']),
            ('name', orm['elections.ElectionInstanceModule:name']),
            ('slug', orm['elections.ElectionInstanceModule:slug']),
        ))
        db.send_create_signal('elections', ['ElectionInstanceModule'])
        
        # Adding model 'ElectionInstance'
        db.create_table('elections_electioninstance', (
            ('id', orm['elections.ElectionInstance:id']),
            ('council', orm['elections.ElectionInstance:council']),
            ('election_event', orm['elections.ElectionInstance:election_event']),
            ('name', orm['elections.ElectionInstance:name']),
            ('start_date', orm['elections.ElectionInstance:start_date']),
            ('end_date', orm['elections.ElectionInstance:end_date']),
            ('wizard_start_date', orm['elections.ElectionInstance:wizard_start_date']),
            ('website', orm['elections.ElectionInstance:website']),
        ))
        db.send_create_signal('elections', ['ElectionInstance'])
        
        # Adding model 'Party'
        db.create_table('elections_party', (
            ('id', orm['elections.Party:id']),
            ('region', orm['elections.Party:region']),
            ('level', orm['elections.Party:level']),
            ('name', orm['elections.Party:name']),
            ('abbreviation', orm['elections.Party:abbreviation']),
            ('website', orm['elections.Party:website']),
            ('slogan', orm['elections.Party:slogan']),
            ('telephone', orm['elections.Party:telephone']),
            ('email', orm['elections.Party:email']),
            ('goals', orm['elections.Party:goals']),
            ('description', orm['elections.Party:description']),
            ('history', orm['elections.Party:history']),
            ('manifasto_summary', orm['elections.Party:manifasto_summary']),
            ('manifesto', orm['elections.Party:manifesto']),
            ('logo', orm['elections.Party:logo']),
        ))
        db.send_create_signal('elections', ['Party'])
        
        # Adding ManyToManyField 'Candidacy.answers'
        db.create_table('elections_candidacy_answers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('candidacy', models.ForeignKey(orm.Candidacy, null=False)),
            ('answer', models.ForeignKey(orm['questions.Answer'], null=False))
        ))
        
        # Adding ManyToManyField 'Council.chanceries'
        db.create_table('elections_council_chanceries', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('council', models.ForeignKey(orm.Council, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'Party.contacts'
        db.create_table('elections_party_contacts', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('party', models.ForeignKey(orm.Party, null=False)),
            ('user', models.ForeignKey(orm['auth.User'], null=False))
        ))
        
        # Adding ManyToManyField 'ElectionInstance.modules'
        db.create_table('elections_electioninstance_modules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('electioninstance', models.ForeignKey(orm.ElectionInstance, null=False)),
            ('electioninstancemodule', models.ForeignKey(orm.ElectionInstanceModule, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ElectionInstanceQuestion'
        db.delete_table('elections_electioninstancequestion')
        
        # Deleting model 'Council'
        db.delete_table('elections_council')
        
        # Deleting model 'ElectionEvent'
        db.delete_table('elections_electionevent')
        
        # Deleting model 'Candidacy'
        db.delete_table('elections_candidacy')
        
        # Deleting model 'ElectionInstanceParty'
        db.delete_table('elections_electioninstanceparty')
        
        # Deleting model 'ElectionInstanceModule'
        db.delete_table('elections_electioninstancemodule')
        
        # Deleting model 'ElectionInstance'
        db.delete_table('elections_electioninstance')
        
        # Deleting model 'Party'
        db.delete_table('elections_party')
        
        # Dropping ManyToManyField 'Candidacy.answers'
        db.delete_table('elections_candidacy_answers')
        
        # Dropping ManyToManyField 'Council.chanceries'
        db.delete_table('elections_council_chanceries')
        
        # Dropping ManyToManyField 'Party.contacts'
        db.delete_table('elections_party_contacts')
        
        # Dropping ManyToManyField 'ElectionInstance.modules'
        db.delete_table('elections_electioninstance_modules')
        
    
    
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
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'election_party_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'candidates'", 'to': "orm['elections.ElectionInstanceParty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.council': {
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'another_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'chanceries': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'desciption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75'}),
            'foreground_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
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
            'desciption': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'party_due_period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'profile_due_period': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'question_due_period': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.electioninstance': {
            'council': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Council']"}),
            'election_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionEvent']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.ElectionInstanceModule']"}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
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
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_length': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Party']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.electioninstancequestion': {
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'elections.party': {
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'goals': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'history': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'manifasto_summary': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'manifesto': ('django.db.models.fields.CharField', [], {'max_length': '2550', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slogan': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'website': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'questions.answer': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }
    
    complete_apps = ['elections']
