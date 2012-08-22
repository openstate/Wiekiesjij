
from south.db import db
from django.db import models
from questions.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'QuestionSet'
        db.create_table('questions_questionset', (
            ('id', orm['questions.QuestionSet:id']),
            ('name', orm['questions.QuestionSet:name']),
        ))
        db.send_create_signal('questions', ['QuestionSet'])
        
        # Adding model 'Question'
        db.create_table('questions_question', (
            ('id', orm['questions.Question:id']),
            ('title', orm['questions.Question:title']),
            ('frontend_title', orm['questions.Question:frontend_title']),
            ('question_type', orm['questions.Question:question_type']),
            ('weight', orm['questions.Question:weight']),
            ('theme', orm['questions.Question:theme']),
            ('has_no_preference', orm['questions.Question:has_no_preference']),
            ('result_title', orm['questions.Question:result_title']),
            ('help_text', orm['questions.Question:help_text']),
            ('min_num_answers', orm['questions.Question:min_num_answers']),
        ))
        db.send_create_signal('questions', ['Question'])
        
        # Adding model 'QuestionSetQuestion'
        db.create_table('questions_questionsetquestion', (
            ('id', orm['questions.QuestionSetQuestion:id']),
            ('question', orm['questions.QuestionSetQuestion:question']),
            ('questionset', orm['questions.QuestionSetQuestion:questionset']),
            ('position', orm['questions.QuestionSetQuestion:position']),
        ))
        db.send_create_signal('questions', ['QuestionSetQuestion'])
        
        # Adding model 'Answer'
        db.create_table('questions_answer', (
            ('id', orm['questions.Answer:id']),
            ('question', orm['questions.Answer:question']),
            ('value', orm['questions.Answer:value']),
            ('frontoffice_value', orm['questions.Answer:frontoffice_value']),
            ('meta', orm['questions.Answer:meta']),
            ('position', orm['questions.Answer:position']),
        ))
        db.send_create_signal('questions', ['Answer'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'QuestionSet'
        db.delete_table('questions_questionset')
        
        # Deleting model 'Question'
        db.delete_table('questions_question')
        
        # Deleting model 'QuestionSetQuestion'
        db.delete_table('questions_questionsetquestion')
        
        # Deleting model 'Answer'
        db.delete_table('questions_answer')
        
    
    
    models = {
        'questions.answer': {
            'frontoffice_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'frontend_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'has_no_preference': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'result_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'min_num_answers': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'})
        },
        'questions.questionset': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        },
        'questions.questionsetquestion': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'questionset': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.QuestionSet']"})
        }
    }
    
    complete_apps = ['questions']
