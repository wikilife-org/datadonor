from django.conf.urls import patterns, include, url
from django.contrib import admin

from social.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    #Social Mock
    url(r'^reach/mock/', social_reach_mock, name='reach_mock'),
    url(r'^sharing/mock/', social_sharing_mock, name='sharing_mock'),
    url(r'^education/mock/', social_education_mock, name='education_mock'),
    url(r'^work/mock/', social_work_mock, name='work_mock'),

    url(r'^reach/global/', social_reach_global, name='reach_global'),
    url(r'^sharing/global/', social_sharing_global, name='sharing_global'),
    url(r'^education/global/', social_education_global, name='education_global'),
    url(r'^work/global/', social_work_global, name='work_gloobal'),
    
    url(r'^user/gender/(?P<gender>.+)/', user_gender, name='gender'),
    url(r'^reach/', social_reach, name='reach'),
    url(r'^sharing/', social_sharing, name='sharing'),
    url(r'^education/', social_education, name='education'),
    url(r'^work/', social_work, name='work'),


   
)