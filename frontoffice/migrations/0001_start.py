
from south.db import db
from django.db import models
from frontoffice.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'VisitorResult'
        db.create_table('frontoffice_visitorresult', (
            ('id', orm['frontoffice.VisitorResult:id']),
            ('user', orm['frontoffice.VisitorResult:user']),
            ('ipaddress', orm['frontoffice.VisitorResult:ipaddress']),
            ('hash', orm['frontoffice.VisitorResult:hash']),
            ('datetime_stamp', orm['frontoffice.VisitorResult:datetime_stamp']),
            ('visitor_answers', orm['frontoffice.VisitorResult:visitor_answers']),
            ('telephone', orm['frontoffice.VisitorResult:telephone']),
        ))
        db.send_create_signal('frontoffice', ['VisitorResult'])
        
        # Adding model 'CandidateAnswers'
        db.create_table('frontoffice_candidateanswers', (
            ('id', orm['frontoffice.CandidateAnswers:id']),
            ('candidate', orm['frontoffice.CandidateAnswers:candidate']),
            ('candidate_answers', orm['frontoffice.CandidateAnswers:candidate_answers']),
            ('candidate_question_scores', orm['frontoffice.CandidateAnswers:candidate_question_scores']),
            ('candidates_score', orm['frontoffice.CandidateAnswers:candidates_score']),
        ))
        db.send_create_signal('frontoffice', ['CandidateAnswers'])
        
        # Adding ManyToManyField 'CandidateAnswers.visitor_result'
        db.create_table('frontoffice_candidateanswers_visitor_result', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('candidateanswers', models.ForeignKey(orm.CandidateAnswers, null=False)),
            ('visitorresult', models.ForeignKey(orm.VisitorResult, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'VisitorResult'
        db.delete_table('frontoffice_visitorresult')
        
        # Deleting model 'CandidateAnswers'
        db.delete_table('frontoffice_candidateanswers')
        
        # Dropping ManyToManyField 'CandidateAnswers.visitor_result'
        db.delete_table('frontoffice_candidateanswers_visitor_result')
        
    
    
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
        'frontoffice.candidateanswers': {
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'candidate_answers': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'}),
            'candidate_question_scores': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'}),
            'candidates_score': ('django.db.models.fields.PositiveIntegerField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'visitor_result': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['frontoffice.VisitorResult']"})
        },
        'frontoffice.visitorresult': {
            'datetime_stamp': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'hash': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '32'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ipaddress': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'telephone': ('django.db.models.fields.CharField', [], {'max_length': '12', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'visitor_answers': ('django.db.models.fields.CharField', [], {'max_length': '2255', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['frontoffice']
