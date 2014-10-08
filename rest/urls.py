from django.conf.urls import patterns, include, url
from django.contrib import admin

from rest.views import *

admin.autodiscover()


urlpatterns = patterns('',
    

    #REST
    url(r'^authorize/', authorize, name='authorize'),
    #Health
    url(r'^health/oxygen_saturation/', oxygen_saturation, name='oxygen_saturation'),
    url(r'^health/blood_glucose/', blood_glucose, name='blood_glucose'),
    url(r'^health/blood_alcohol_content/', blood_alcohol_content, name='blood_alcohol_content'),
    url(r'^health/blood_type/', blood_type, name='blood_type'),
    url(r'^health/body_temperature/', body_temperature, name='body_temperature'),
    
    #Physical
    url(r'^physical/heart_rate/', heart_rate, name='heart_rate'),
    url(r'^physical/step_count/', step_count, name='step_count'),
    url(r'^physical/distance/', distance, name='distance'),
    url(r'^physical/activity_count/', activity_count, name='activity_count'),
    url(r'^physical/active_energy/', active_energy, name='active_energy'),
    url(r'^physical/nike_fuel/', nike_fuel, name='nike_fuel'),
    
    #Nutrition
    url(r'^nutrition/bmi/', bmi, name='bmi'),
    url(r'^nutrition/fat_total/', fat_total, name='fat_total'),
    url(r'^nutrition/fiber/', fiber, name='fiber'),
    url(r'^nutrition/sugar/', sugar, name='sugar'),
    url(r'^nutrition/calories/', calories, name='calories'),
    url(r'^nutrition/protein/', protein, name='protein'),
    url(r'^nutrition/carbohydrates/', carbohydrates, name='carbohydrates'),
    
    #Profile
    url(r'^profile/height/', height, name='height'), 
    url(r'^profile/gender/', gender, name='gender'), 
    url(r'^profile/date_of_birth/', date_of_birth, name='date_of_birth'), 

)