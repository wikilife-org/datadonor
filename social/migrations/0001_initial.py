# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Profile'
        db.create_table(u'social_profile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(related_name='profile', unique=True, to=orm['auth.User'])),
            ('account_id', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('email', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('age', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_of_birth', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['Profile'])

        # Adding model 'SocialUserAggregatedData'
        db.create_table(u'social_socialuseraggregateddata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(blank=True, related_name='social_aggregated_data', unique=True, null=True, to=orm['auth.User'])),
            ('facebook_friend_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_post_weekly_avg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_likes_weekly_avg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('twitter_followers_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('twitter_tweets_count_last_seven_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('twitter_retweets_count_last_seven_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gplus_contacts_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('linkedin_connections_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('foursquare_friends_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('education_level', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('education_degree', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('work_experience_years', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['SocialUserAggregatedData'])

        # Adding model 'GlobalEducationDistribution'
        db.create_table(u'social_globaleducationdistribution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('elementary', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('high_school', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('junior_collage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tech', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('university', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('master', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('phd', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['GlobalEducationDistribution'])

        # Adding model 'GlobalWorkExperinceDistribution'
        db.create_table(u'social_globalworkexperincedistribution', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('range_15_25', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('range_25_35', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('range_36_45', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('range_46_55', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('range_56_65', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['GlobalWorkExperinceDistribution'])

        # Adding model 'SocialGlobalAggregatedData'
        db.create_table(u'social_socialglobalaggregateddata', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('avg_facebook_friend_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_post_weekly_avg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('facebook_likes_weekly_avg', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_twitter_followers_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_twitter_tweets_count_last_seven_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_twitter_retweets_count_last_seven_days', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('gplus_contacts_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_linkedin_connections_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('avg_foursquare_connections_count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('education', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.GlobalEducationDistribution'], unique=True)),
            ('work_experience', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['social.GlobalWorkExperinceDistribution'], unique=True)),
            ('create_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('update_time', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
        ))
        db.send_create_signal(u'social', ['SocialGlobalAggregatedData'])

        # Adding model 'DegreeLevel'
        db.create_table(u'social_degreelevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250)),
            ('elementary', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('high_school', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('junior_collage', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('tech', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('university', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('master', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('phd', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'social', ['DegreeLevel'])


    def backwards(self, orm):
        # Deleting model 'Profile'
        db.delete_table(u'social_profile')

        # Deleting model 'SocialUserAggregatedData'
        db.delete_table(u'social_socialuseraggregateddata')

        # Deleting model 'GlobalEducationDistribution'
        db.delete_table(u'social_globaleducationdistribution')

        # Deleting model 'GlobalWorkExperinceDistribution'
        db.delete_table(u'social_globalworkexperincedistribution')

        # Deleting model 'SocialGlobalAggregatedData'
        db.delete_table(u'social_socialglobalaggregateddata')

        # Deleting model 'DegreeLevel'
        db.delete_table(u'social_degreelevel')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'social.degreelevel': {
            'Meta': {'object_name': 'DegreeLevel'},
            'elementary': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'high_school': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'junior_collage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'master': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tech': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'university': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'social.globaleducationdistribution': {
            'Meta': {'object_name': 'GlobalEducationDistribution'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'elementary': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'high_school': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'junior_collage': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'master': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'phd': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'tech': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'university': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'social.globalworkexperincedistribution': {
            'Meta': {'object_name': 'GlobalWorkExperinceDistribution'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'range_15_25': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range_25_35': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range_36_45': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range_46_55': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'range_56_65': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        u'social.profile': {
            'Meta': {'object_name': 'Profile'},
            'account_id': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'age': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_of_birth': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'profile'", 'unique': 'True', 'to': u"orm['auth.User']"})
        },
        u'social.socialglobalaggregateddata': {
            'Meta': {'object_name': 'SocialGlobalAggregatedData'},
            'avg_facebook_friend_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_foursquare_connections_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_linkedin_connections_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_twitter_followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_twitter_retweets_count_last_seven_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'avg_twitter_tweets_count_last_seven_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'education': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.GlobalEducationDistribution']", 'unique': 'True'}),
            'facebook_likes_weekly_avg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_post_weekly_avg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gplus_contacts_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'work_experience': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['social.GlobalWorkExperinceDistribution']", 'unique': 'True'})
        },
        u'social.socialuseraggregateddata': {
            'Meta': {'object_name': 'SocialUserAggregatedData'},
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'education_degree': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'education_level': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'facebook_friend_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_likes_weekly_avg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'facebook_post_weekly_avg': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'foursquare_friends_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gplus_contacts_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'linkedin_connections_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_followers_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_retweets_count_last_seven_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'twitter_tweets_count_last_seven_days': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'update_time': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'blank': 'True', 'related_name': "'social_aggregated_data'", 'unique': 'True', 'null': 'True', 'to': u"orm['auth.User']"}),
            'work_experience_years': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['social']