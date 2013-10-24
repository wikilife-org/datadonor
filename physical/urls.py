from django.conf.urls.defaults import patterns, url
from django.contrib import admin

from physical.views import *

admin.autodiscover()

urlpatterns = patterns('',

    url(r'^physical/exercise/top/', physical_exercise, name='physical_exercise'),
    url(r'^physical/exercise/user/', physical_user_exercise, name='physical_user_exercise'),
    url(r'^physical/exercise/steps/distribution', physical_steps_distribution, name='physical_steps_distribution'),
    url(r'^physical/exercise/miles/distribution', physical_miles_distribution, name='physical_miles_distribution'),
    url(r'^physical/exercise/hours/distribution', physical_hours_distribution, name='physical_hours_distribution'),

    #Physical Mock
    url(r'^physical/exercise/top/mock/', physical_exercise_mock, name='physical_exercise_mock'),
    url(r'^physical/exercise/user/mock/', physical_user_exercise_mock, name='physical_user_exercise_mock'),
    url(r'^physical/exercise/steps/distribution/mock/', physical_steps_distribution_mock, name='physical_steps_distribution_mock'),
    url(r'^physical/exercise/miles/distribution/mock/', physical_miles_distribution_mock, name='physical_miles_distribution_mock'),
    url(r'^physical/exercise/hours/distribution/mock/', physical_hours_distribution_mock, name='physical_hours_distribution_mock'),

)