
from south.db import db
from django.db import models
from elections.models import *

class Migration:
    
    depends_on = (
        ("questions", "0001_initial"),
    )
        
    def forwards(self, orm):
        
        # Adding model 'ElectionInstanceQuestion'
        db.create_table('elections_electioninstancequestion', (
            ('id', orm['elections.ElectionInstanceQuestion:id']),
            ('election_instance', orm['elections.ElectionInstanceQuestion:election_instance']),
            ('question', orm['elections.ElectionInstanceQuestion:question']),
            ('locked', orm['elections.ElectionInstanceQuestion:locked']),
        ))
        db.send_create_signal('elections', ['ElectionInstanceQuestion'])
        
        # Adding model 'ElectionEvent'
        db.create_table('elections_electionevent', (
            ('id', orm['elections.ElectionEvent:id']),
            ('name', orm['elections.ElectionEvent:name']),
            ('parent_region', orm['elections.ElectionEvent:parent_region']),
            ('level', orm['elections.ElectionEvent:level']),
        ))
        db.send_create_signal('elections', ['ElectionEvent'])
        
        # Adding model 'Candidacy'
        db.create_table('elections_candidacy', (
            ('id', orm['elections.Candidacy:id']),
            ('party', orm['elections.Candidacy:party']),
            ('politician', orm['elections.Candidacy:politician']),
            ('election_instance', orm['elections.Candidacy:election_instance']),
            ('position', orm['elections.Candidacy:position']),
        ))
        db.send_create_signal('elections', ['Candidacy'])
        
        # Adding model 'Council'
        db.create_table('elections_council', (
            ('id', orm['elections.Council:id']),
            ('name', orm['elections.Council:name']),
            ('region', orm['elections.Council:region']),
            ('level', orm['elections.Council:level']),
            ('chancery', orm['elections.Council:chancery']),
        ))
        db.send_create_signal('elections', ['Council'])
        
        # Adding model 'ElectionInstance'
        db.create_table('elections_electioninstance', (
            ('id', orm['elections.ElectionInstance:id']),
            ('council', orm['elections.ElectionInstance:council']),
            ('election_event', orm['elections.ElectionInstance:election_event']),
        ))
        db.send_create_signal('elections', ['ElectionInstance'])
        
        # Adding model 'Party'
        db.create_table('elections_party', (
            ('id', orm['elections.Party:id']),
            ('name', orm['elections.Party:name']),
            ('contact', orm['elections.Party:contact']),
            ('region', orm['elections.Party:region']),
            ('level', orm['elections.Party:level']),
        ))
        db.send_create_signal('elections', ['Party'])
        
        # Adding ManyToManyField 'Candidacy.answers'
        db.create_table('elections_candidacy_answers', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('candidacy', models.ForeignKey(orm.Candidacy, null=False)),
            ('answer', models.ForeignKey(orm['questions.Answer'], null=False))
        ))
        
        # Adding ManyToManyField 'ElectionInstance.parties'
        db.create_table('elections_electioninstance_parties', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('electioninstance', models.ForeignKey(orm.ElectionInstance, null=False)),
            ('party', models.ForeignKey(orm.Party, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'ElectionInstanceQuestion'
        db.delete_table('elections_electioninstancequestion')
        
        # Deleting model 'ElectionEvent'
        db.delete_table('elections_electionevent')
        
        # Deleting model 'Candidacy'
        db.delete_table('elections_candidacy')
        
        # Deleting model 'Council'
        db.delete_table('elections_council')
        
        # Deleting model 'ElectionInstance'
        db.delete_table('elections_electioninstance')
        
        # Deleting model 'Party'
        db.delete_table('elections_party')
        
        # Dropping ManyToManyField 'Candidacy.answers'
        db.delete_table('elections_candidacy_answers')
        
        # Dropping ManyToManyField 'ElectionInstance.parties'
        db.delete_table('elections_electioninstance_parties')
        
    
    
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
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'candidates'", 'null': 'True', 'to': "orm['elections.Party']"}),
            'politician': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.council': {
            'chancery': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elections.electionevent': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'parent_region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'elections.electioninstance': {
            'council': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.Council']"}),
            'election_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionEvent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.Party']"}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        },
        'elections.electioninstancequestion': {
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'elections.party': {
            'contact': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'level': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'questions.answer': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['elections']
