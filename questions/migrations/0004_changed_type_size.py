
from south.db import db
from django.db import models
from questions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Question.question_type'
        # (to signature: django.db.models.fields.CharField(max_length=10))
        db.alter_column('questions_question', 'question_type', orm['questions.question:question_type'])
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Question.question_type'
        # (to signature: django.db.models.fields.CharField(max_length=1))
        db.alter_column('questions_question', 'question_type', orm['questions.question:question_type'])
        
    
    
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
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        },
        'questions.questionset': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        },
        'questions.questionsetquestion': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.QuestionSet']"})
        }
    }
    
    complete_apps = ['questions']
