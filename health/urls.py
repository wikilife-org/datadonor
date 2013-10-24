from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from health.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    #Cronical Conditions

    url(r'^cronical_conditions/global/top_5/mock/', cronical_conditions_ranking_global_mock, name='cronical_conditions_ranking_global_mock'),
    url(r'^cronical_conditions/user/mock/', cronical_conditions_by_user_mock, name='cronical_conditions_by_user_mock'),
    url(r'^cronical_conditions/list/mock/', cronical_conditions_list_mock, name='cronical_conditions_list_mock'),


    url(r'^cronical_conditions/global/top_5/', cronical_conditions_ranking_global, name='cronical_conditions_ranking_global'),
    url(r'^cronical_conditions/user/', cronical_conditions_by_user, name='cronical_conditions_by_user'),
    url(r'^cronical_conditions/list/', cronical_conditions_list, name='cronical_conditions_list'),


    #Complaints
    url(r'^complaints/global/top_5/mock/', complaints_ranking_global_mock, name='complaints_ranking_global_mock'),
    url(r'^complaints/list/mock/', complaints_list_mock, name='complaints_list_mock'),
    url(r'^complaints/user/mock/', complaints_by_user_mock, name='complaints_by_user_mock'),
  
    url(r'^complaints/global/top_5/', complaints_ranking_global, name='complaints_ranking_global'),
    url(r'^complaints/list/', complaints_list, name='complaints_list'),
    url(r'^complaints/user/', complaints_by_user, name='complaints_by_user'),
   
  
    #Blood Type
    url(r'^blood_type/global/distribution/mock/', bood_type_distribution_global_mock, name='bood_type_distribution_global_mock'),
    url(r'^blood_type/user/mock/', bood_type_by_user_mock, name='bood_type_by_user_mock'),
    
    url(r'^blood_type/global/distribution/', bood_type_distribution_global, name='bood_type_distribution_global'),
    url(r'^blood_type/user/', bood_type_by_user, name='bood_type_by_user'),


    #Sleep
    url(r'^sleep/global/distribution/mock/', sleep_distribution_global_mock, name='sleep_distribution_global_mock'),
    url(r'^sleep/user/distribution/mock/', sleep_distribution_by_user_mock, name='sleep_distribution_by_user_mock'),

    url(r'^sleep/global/distribution/', sleep_distribution_global, name='sleep_distribution_global'),
    url(r'^sleep/user/distribution/', sleep_distribution_by_user, name='sleep_distribution_by_user'),

    #Emotions
    url(r'^emotions/global/top_5/mock/', emotions_ranking_global_mock, name='emotions_ranking_global_mock'),
    url(r'^emotions/list/mock/', emotions_list_mock, name='emotions_list_mock'),
    url(r'^emotions/user/mock/', emotions_by_user_mock, name='emotions_by_user_mock'),
  
    url(r'^emotions/global/top_5/', emotions_ranking_global, name='emotions_ranking_global'),
    url(r'^emotions/list/', emotions_list, name='emotions_list'),
    url(r'^emotions/user/', emotions_by_user, name='emotions_by_user'),
      
    #Mood
    url(r'^mood/global/avg/mock/', mood_avg_global_mock, name='mood_avg_global_mock'),
    url(r'^mood/user/avg/mock/', mood_avg_by_user_mock, name='mood_avg_by_user_mock'),   

    url(r'^mood/global/avg/', mood_avg_global, name='mood_avg_global'),
    url(r'^mood/user/avg/', mood_avg_by_user, name='mood_avg_by_user'),
    
)