from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from genomics.views import *

admin.autodiscover()

urlpatterns = patterns('',

    #Genomics Mock
    url(r'^traits/mock/', genomics_traits_mock, name='genomics_traits_mock'),
    url(r'^drugs/mock/', genomics_drugs_mock, name='genomics_drugs_mock'),
    url(r'^risks/mock/', genomics_risks_mock, name='genomics_risks_mock'),
   
    url(r'^traits/', genomics_traits, name='genomics_traits'),
    url(r'^drugs/', genomics_drugs, name='genomics_drugs'),
    url(r'^risks/', genomics_risks, name='genomics_risks'),

)