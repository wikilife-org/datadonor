from django.conf.urls import patterns, include, url
from django.contrib import admin

from data.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    url(r'^download/', download, name='download'),

)