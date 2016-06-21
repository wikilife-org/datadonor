from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest.views import *

admin.autodiscover()


urlpatterns = patterns('',
    

    #REST
    url(r'^authorize/', authorize, name='authorize'),
    #Health
    url(r'^log/', log, name='log'),
    
    

)