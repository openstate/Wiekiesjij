# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):

        # Adding field 'Candidacy.elected'
        db.add_column('elections_candidacy', 'elected', self.gf('django.db.models.fields.NullBooleanField')(null=True, blank=True), keep_default=False)

        print "ACHTUNG: not removing electioninstance_questions. No guarantees about model<>db sync now."
        # Removing M2M table for field questions on 'electioninstance'
        #db.delete_table('elections_electioninstance_questions')

        print "ACHTUNG: not removing electioninstance_parties"
        # Removing M2M table for field parties on 'electioninstance'
        #db.delete_table('elections_electioninstance_parties')


    def backwards(self, orm):

        # Deleting field 'Candidacy.elected'
        db.delete_column('elections_candidacy', 'elected')

        print "ACHTUNG: not adding electioninstance_questions. No guarantees about model<>db sync now."
        # Adding M2M table for field questions on 'electioninstance'
        #db.create_table('elections_electioninstance_questions', (
        #    ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
        #    ('electioninstance', models.ForeignKey(orm['elections.electioninstance'], null=False)),
        #    ('question', models.ForeignKey(orm['questions.question'], null=False))
        #))
        #db.create_unique('elections_electioninstance_questions', ['electioninstance_id', 'question_id'])

        print "ACHTUNG: not adding electioninstance_parties"
        # Adding M2M table for field parties on 'electioninstance'
        #db.create_table('elections_electioninstance_parties', (
        #    ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
        #    ('electioninstance', models.ForeignKey(orm['elections.electioninstance'], null=False)),
        #    ('party', models.ForeignKey(orm['elections.party'], null=False))
        #))
        #db.create_unique('elections_electioninstance_parties', ['electioninstance_id', 'party_id'])


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'elections.candidacy': {
            'Meta': {'unique_together': "(('election_party_instance', 'candidate'), ('election_party_instance', 'position'))", 'object_name': 'Candidacy'},
            'answers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['questions.Answer']", 'symmetrical': 'False'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'elections'", 'to': "orm['auth.User']"}),
            'elected': ('django.db.models.fields.NullBooleanField', [], {'null': 'True', 'blank': 'True'}),
            'election_party_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'candidates'", 'to': "orm['elections.ElectionInstanceParty']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.council': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Council'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'another_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'background_color': ('django.db.models.fields.CharField', [], {'max_length': '6', 'null': 'True', 'blank': 'True'}),
            'chanceries': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'councils'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
            'credit': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0', 'max_length': '8'}),
            'credit_warning': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
        'elections.councilevent': {
            'Meta': {'object_name': 'CouncilEvent'},
            'council': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'events'", 'to': "orm['elections.Council']"}),
            'event_datetime': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'location': ('django.db.models.fields.TextField', [], {}),
            'message': ('django.db.models.fields.CharField', [], {'max_length': '140'}),
            'originator': ('django.db.models.fields.CharField', [], {'max_length': '11'}),
            'sent_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '60'})
        },
        'elections.electionevent': {
            'Meta': {'object_name': 'ElectionEvent'},
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
            'Meta': {'object_name': 'ElectionInstance'},
            'council': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instances'", 'to': "orm['elections.Council']"}),
            'election_event': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionEvent']"}),
            'end_date': ('django.db.models.fields.DateTimeField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['elections.ElectionInstanceModule']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'num_lists': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'parties': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['elections.Party']", 'through': "orm['elections.ElectionInstanceParty']", 'symmetrical': 'False'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['questions.Question']", 'null': 'True', 'through': "orm['elections.ElectionInstanceQuestion']", 'blank': 'True'}),
            'start_date': ('django.db.models.fields.DateTimeField', [], {}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'wizard_start_date': ('django.db.models.fields.DateTimeField', [], {})
        },
        'elections.electioninstancemodule': {
            'Meta': {'ordering': "('name',)", 'object_name': 'ElectionInstanceModule'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'})
        },
        'elections.electioninstanceparty': {
            'Meta': {'unique_together': "(('election_instance', 'position'),)", 'object_name': 'ElectionInstanceParty'},
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instance_parties'", 'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_length': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'election_instance_parties'", 'to': "orm['elections.Party']"}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {})
        },
        'elections.electioninstancequestion': {
            'Meta': {'ordering': "('position', 'question__id')", 'object_name': 'ElectionInstanceQuestion'},
            'election_instance': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstance']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'locked': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['questions.Question']"})
        },
        'elections.electioninstancequestionanswer': {
            'Meta': {'unique_together': "(('election_instance_question', 'candidate'),)", 'object_name': 'ElectionInstanceQuestionAnswer'},
            'answer_value': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'election_instance_question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['elections.ElectionInstanceQuestion']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        'elections.party': {
            'Meta': {'object_name': 'Party'},
            'abbreviation': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'address_city': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_number': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_postalcode': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_street': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'contacts': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'parties'", 'symmetrical': 'False', 'to': "orm['auth.User']"}),
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
        'elections.smssubscription': {
            'Meta': {'object_name': 'SmsSubscription'},
            'council_event': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sms_subscriptions'", 'to': "orm['elections.CouncilEvent']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '15'})
        },
        'questions.answer': {
            'Meta': {'ordering': "('position', 'question')", 'object_name': 'Answer'},
            'frontoffice_value': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'meta': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'position': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'answers'", 'to': "orm['questions.Question']"}),
            'value': ('django.db.models.fields.TextField', [], {})
        },
        'questions.question': {
            'Meta': {'object_name': 'Question'},
            'frontend_title': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'has_no_preference': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'help_text': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question_type': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'result_title': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'theme': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'weight': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'})
        }
    }

    complete_apps = ['elections']
