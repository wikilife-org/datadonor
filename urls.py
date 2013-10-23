from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from social.facebook import facebook_view
from physical.views import *
from social.views import *

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'google7d1bd3580ebd5b1b.html$', greg, name='greg'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^maqueta/$', mock, name='maqueta'),
    url(r'^wizard/$', wizard, name='wizard'),
    url(r'^end-wizard/$', end_wizard, name='end_wizard'),
    url(r'^iagree/$', iagree, name='iagree'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^comming/', comming, name='comming'),
    url(r'', include('social_auth.urls')),
    
    url(r'^social/', include('social.urls')),
    url(r'^health/', include('health.urls')),
    
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

    url(r'^nutrition/nutrients/', nutrition_nutrients, name='nutrition_nutrients'),
    url(r'^nutrition/weight/', nutrition_weight, name='nutrition_weight'),
    url(r'^nutrition/height/', nutrition_height, name='nutrition_height'),
    url(r'^nutrition/bmi/', nutrition_bmi, name='nutrition_bmi'),
    
    url(r'^wikilife/push', wikilife_push, name='wikilife_push'),
    url(r'^wikilife/pull', wikilife_pull, name='wikilife_pull'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)