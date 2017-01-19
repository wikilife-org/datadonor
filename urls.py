from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls import patterns, include, url
#from social.facebook import facebook_view
from views import *
from reports.views import *
from reports.views import miles_history

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home_bye, name='home_bye'),
    

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)