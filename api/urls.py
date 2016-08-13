from django.conf.urls import patterns, include, url
from django.contrib import admin

from api.views import *

admin.autodiscover()


urlpatterns = patterns('',
    
    
    #New API
    url(r'^register/', register, name='register'),
    url(r'^device/add/', add_device, name='add_device'),
    url(r'^device/delete/', delete_device, name='delete_device'),
    
    url(r'^log/add/', add_log, name='add_log'),
    url(r'^log/get/', get_log, name='get_log'),
    url(r'^log/edit/', edit_log, name='edit_log'),
    url(r'^log/delete/', delete_log, name='delete_log'),
    url(r'^log/image/add/', add_image, name='add_image'),
    
    url(r'^timeline/', get_timeline, name='get_timeline'),
    url(r'^profile/', get_profile, name='get_profile'),
    
    

)