from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from social.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    
    #Social Mock
    url(r'^reach/mock/', social_reach_mock, name='reach_mock'),
    url(r'^sharing/mock/', social_sharing_mock, name='sharing_mock'),
    url(r'^education/mock/', social_education_mock, name='education_mock'),
    url(r'^work/mock/', social_work_mock, name='work_mock'),


    url(r'^reach/', social_reach, name='reach'),
    url(r'^sharing/', social_sharing, name='sharing'),
    url(r'^education/', social_education, name='education'),
    url(r'^work/', social_work, name='work'),


   
)