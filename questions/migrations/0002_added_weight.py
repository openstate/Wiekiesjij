
from south.db import db
from django.db import models
from questions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Question.theme'
        db.add_column('questions_question', 'theme', orm['questions.question:theme'])
        
        # Adding field 'Question.weight'
        db.add_column('questions_question', 'weight', orm['questions.question:weight'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Question.theme'
        db.delete_column('questions_question', 'theme')
        
        # Deleting field 'Question.weight'
        db.delete_column('questions_question', 'weight')
        
    
    
    models = {
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
        },
        'questions.questionset': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        }
    }
    
    complete_apps = ['questions']
