
from django.conf.urls import patterns, include, url
from django.contrib import admin

from stats.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^exercise/$', go_exercise_stats, name='go_exercise_stats'),
    url(r'^exercise/data', go_exercise_data, name='go_exercise_data'),
    
    url(r'^health/$', go_health_stats, name='go_health_stats'),
    url(r'^health/data', go_health_data, name='go_health_data'),
    
    url(r'^nutrition/$', go_nutrition_stats, name='go_nutrition_stats'),
    url(r'^nutrition/data', go_nutrition_data, name='go_nutrition_data'),
    
    url(r'^social/$', go_social_stats, name='go_social_stats'),
    url(r'^social/data', go_social_data, name='go_social_data'),

    url(r'^contact/$', go_contact, name='go_contact'),
)