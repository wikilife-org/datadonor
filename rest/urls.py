from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    #REST Mock
    url(r'^health/mock/', health_mock, name='health_mock'),
    url(r'^physical/mock/', physical_mock, name='physical_mock'),
    url(r'^nutrition/mock/', nutrition_mock, name='nutrition_mock'),
    url(r'^profile/mock/', profile_mock, name='profile_mock'),
  
    #REST
    url(r'^health/', health, name='health'),
    url(r'^physical/', physical, name='physical'),
    url(r'^nutrition/', nutrition, name='nutrition'),
    url(r'^profile/', profile, name='profile'), 
    
)