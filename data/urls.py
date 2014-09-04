from django.conf.urls import patterns, include, url
from django.contrib import admin

from data.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^/', download, name='download'),
    url(r'^history/steps/json/', history_steps, name='history_steps'),
    url(r'^history/distance/json/', history_distance, name='history_distance'),
    url(r'^history/steps/csv/', history_steps_csv, name='history_steps_csv'),
    url(r'^history/distance/csv/', history_distance_csv, name='history_distance_csv'),

)