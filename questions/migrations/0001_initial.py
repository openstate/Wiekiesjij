
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
            ('question_type', orm['questions.Question:question_type']),
            ('weight', orm['questions.Question:weight']),
            ('theme', orm['questions.Question:theme']),
        ))
        db.send_create_signal('questions', ['Question'])
        
        # Adding model 'Answer'
        db.create_table('questions_answer', (
            ('id', orm['questions.Answer:id']),
            ('question', orm['questions.Answer:question']),
            ('value', orm['questions.Answer:value']),
        ))
        db.send_create_signal('questions', ['Answer'])
        
        # Adding ManyToManyField 'QuestionSet.question'
        db.create_table('questions_questionset_question', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('questionset', models.ForeignKey(orm.QuestionSet, null=False)),
            ('question', models.ForeignKey(orm.Question, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'QuestionSet'
        db.delete_table('questions_questionset')
        
        # Deleting model 'Question'
        db.delete_table('questions_question')
        
        # Deleting model 'Answer'
        db.delete_table('questions_answer')
        
        # Dropping ManyToManyField 'QuestionSet.question'
        db.delete_table('questions_questionset_question')
        
    
    
    models = {
        'questions.answer': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
            'theme': ('django.db.models.fields.CharField', [], {'max_length': '255',})
        },
        'questions.questionset': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'question': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Question']"})
        }
    }
    
    complete_apps = ['questions']
