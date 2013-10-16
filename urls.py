from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from social.views import *
from social.facebook import facebook_view

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
    
    url(r'^social/reach/', social_reach, name='reach'),
    url(r'^social/sharing/', social_sharing, name='sharing'),
    url(r'^social/education/', social_education, name='education'),
    url(r'^social/work/', social_work, name='work'),

    url(r'^physical/exercise/top/', physical_exercise, name='physical_exercise'),
    url(r'^physical/exercise/user/', physical_user_exercise, name='physical_user_exercise'),
    url(r'^physical/exercise/steps/distribution', physical_steps_distribution, name='physical_steps_distribution'),
    url(r'^physical/exercise/miles/distribution', physical_miles_distribution, name='physical_miles_distribution'),
    url(r'^physical/exercise/hours/distribution', physical_hours_distribution, name='physical_hours_distribution'),

    url(r'^nutrition/nutrients/', nutrition_nutrients, name='nutrition_nutrients'),
    url(r'^nutrition/weight/', nutrition_weight, name='nutrition_weight'),
    url(r'^nutrition/height/', nutrition_height, name='nutrition_height'),
    url(r'^nutrition/bmi/', nutrition_bmi, name='nutrition_bmi'),
    
    url(r'^wikilife/push', wikilife_push, name='wikilife_push'),
    url(r'^wikilife/pull', wikilife_pull, name='wikilife_pull'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)