
from south.db import db
from django.db import models
from questions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Question.frontend_title'
        db.add_column('questions_question', 'frontend_title', orm['questions.question:frontend_title'])
        
        # Adding field 'Question.has_no_preference'
        db.add_column('questions_question', 'has_no_preference', orm['questions.question:has_no_preference'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Question.frontend_title'
        db.delete_column('questions_question', 'frontend_title')
        
        # Deleting field 'Question.has_no_preference'
        db.delete_column('questions_question', 'has_no_preference')
        
    
    
    models = {
        'questions.answer': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'frontend_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'has_no_preference': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'questions.questionset': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        }
    }
    
    complete_apps = ['questions']
