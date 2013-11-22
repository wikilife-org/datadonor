from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from genomics.views import *

admin.autodiscover()

urlpatterns = patterns('',

    #Genomics Mock
    url(r'^traits/global/mock/', genomics_traits_global_mock, name='genomics_traits_global_mock'),
    url(r'^traits/user/mock/', genomics_traits_by_user_mock, name='genomics_traits_by_user_mock'),

    url(r'^drugs/global/mock/', genomics_drugs_global_mock, name='genomics_drugs_global_mock'),
    url(r'^drugs/user/mock/', genomics_drugs_by_user_mock, name='genomics_drugs_by_user_mock'),
    
    url(r'^risks/global/mock/', genomics_risks_global_mock, name='genomics_risks_global_mock'),
    url(r'^risks/user/mock/', genomics_risks_by_user_mock, name='genomics_risks_by_user_mock'),
   
   
   
    url(r'^traits/global/', genomics_traits_global, name='genomics_traits_global'),
    url(r'^traits/user/', genomics_traits_by_user, name='genomics_traits_by_user'),

    url(r'^drugs/global/', genomics_drugs_global, name='genomics_drugs_global'),
    url(r'^drugs/user/', genomics_drugs_by_user, name='genomics_drugs_by_user'),
    
    url(r'^risks/global/', genomics_risks_global, name='genomics_risks_global'),
    url(r'^risks/user/', genomics_risks_by_user, name='genomics_risks_by_user'),

)