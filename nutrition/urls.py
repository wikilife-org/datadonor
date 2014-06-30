from django.conf.urls import patterns, include, url
from django.contrib import admin

from nutrition.views import *

admin.autodiscover()

urlpatterns = patterns('',

    #Nutrition Mock

    url(r'^nutrients/mock/', nutrition_nutrients_mock, name='nutrition_nutrients_mock'),
    url(r'^nutrients/global/distribution/mock/', nutrition_global_nutrients_mock, name='nutrition_global_nutrients_mock'),
    url(r'^nutrients/user/distribution/mock/', nutrition_user_nutrients_mock, name='nutrition_user_nutrients_mock'),

    url(r'^weight/mock/', nutrition_weight_mock, name='nutrition_weight_mock'),
    url(r'^weight/global/mock/', nutrition_global_weight_mock, name='nutrition_global_weight_mock'),
    url(r'^weight/user/mock/', nutrition_user_weight_mock, name='nutrition_user_weight_mock'),
    
    url(r'^height/mock/', nutrition_height_mock, name='nutrition_height_mock'),
    url(r'^height/global/mock/', nutrition_global_height_mock, name='nutrition_global_height_mock'),
    url(r'^height/user/mock/', nutrition_user_height_mock, name='nutrition_user_height_mock'),
    
    url(r'^bmi/mock/', nutrition_bmi_mock, name='nutrition_bmi_mock'),
    url(r'^bmi/global/mock/', nutrition_global_bmi_mock, name='nutrition_global_bmi_mock'),
    url(r'^bmi/user/mock/', nutrition_user_bmi_mock, name='nutrition_user_bmi_mock'),


    url(r'^nutrients/global/distribution/', nutrition_global_nutrients, name='nutrition_global_nutrients'),
    url(r'^nutrients/user/distribution/', nutrition_user_nutrients, name='nutrition_user_nutrients'),
    url(r'^nutrients/', nutrition_nutrients, name='nutrition_nutrients'),

    url(r'^weight/', nutrition_weight, name='nutrition_weight'),
    url(r'^weight/global/', nutrition_global_weight, name='nutrition_global_weight'),
    url(r'^weight/user/', nutrition_user_weight, name='nutrition_user_weight'),
    
    url(r'^height/', nutrition_height, name='nutrition_height'),
    url(r'^height/global/', nutrition_global_height, name='nutrition_global_height'),
    url(r'^height/user/', nutrition_user_height, name='nutrition_user_height'),
    
    url(r'^bmi/', nutrition_bmi, name='nutrition_bmi'),
    url(r'^bmi/global/', nutrition_global_bmi, name='nutrition_global_bmi'),
    url(r'^bmi/user/', nutrition_user_bmi, name='nutrition_user_bmi'),



)