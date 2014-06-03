from django.conf.urls import patterns, include, url
from django.contrib import admin

from reports.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    
    #Social Mock
    url(r'^user/physical/(?P<user_id>.+)/', report_for_user_exercise, name='report_for_user_exercise'),
    url(r'^user/social/(?P<user_id>.+)/', report_for_user_social, name='report_for_user_social'),
 
)