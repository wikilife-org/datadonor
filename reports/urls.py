from django.conf.urls import patterns, include, url
from django.contrib import admin

from reports.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^user/physical/(?P<user_id>.+)/', report_for_user_exercise, name='report_for_user_exercise'),
    url(r'^user/social/(?P<user_id>.+)/', report_for_user_social, name='report_for_user_social'),
    url(r'^user/health/(?P<user_id>.+)/', report_for_user_health, name='report_for_user_health'),
    url(r'^user/nutrition/(?P<user_id>.+)/', report_for_user_nutrition, name='report_for_user_nutrition'),
    url(r'^user/genomics/(?P<user_id>.+)/', report_for_user_genomics, name='report_for_user_genomics'),
 
)