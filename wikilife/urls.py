# coding=utf-8

from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from wikilife.views import *

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^sync', wikilife_sync, name='wikilife_sync'),

)