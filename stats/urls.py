
from django.conf.urls import patterns, include, url
from django.contrib import admin

from stats.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^exercise/$', go_exercise_stats, name='go_exercise_stats'),
    url(r'^exercise/data', go_exercise_data, name='go_exercise_data'),

    
)