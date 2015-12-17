from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls import patterns, include, url
#from social.facebook import facebook_view
from views import *
from reports.views import *
from reports.views import miles_history
from stats.views import get_miles

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    #url(r'^graph/$', get_graph, name='graph'),
    url('^send-email/$', send_test_email, name='send_test_email'),
    url('^about-us/$', about, name='about'),
    url(r'google7d1bd3580ebd5b1b.html$', greg, name='greg'),
    url(r'^dashboard/$', dashboard, name='dashboard'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^demo/$', demo, name='demo'),
    url(r'^support-us/$', support_us, name='support_us'),
    url(r'^wizard/$', wizard, name='wizard'),
    url(r'^end-wizard/$', end_wizard, name='end_wizard'),
    url(r'^iagree/$', iagree, name='iagree'),
    url(r'^admin/', include(admin.site.urls)),
    #url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^comming/', comming, name='comming'),
    url(r'^mission/', mission, name='mission'),
    url(r'^team/', team, name='team'),
    url(r'^contact/', contact, name='contact'),
    url(r'^privacy/', privacy, name='privacy'),
    url(r'^terms-of-service/', tos, name='tos'),
    url(r'^learn-more/', learn_more, name='learn-more'),
    url(r'^app/', app, name='app'),
    url(r'^news/', news, name='news'),

    url(r'', include('social_auth.urls')),
    url(r'^genomics/', include('genomics.urls')),
    url(r'^nutrition/', include('nutrition.urls')),
    url(r'^social/', include('social.urls')),
    url(r'^health/', include('health.urls')),
    url(r'^physical/', include('physical.urls')),
    url(r'^wikilife/', include('wikilife.urls')),
    url(r'^reports/', include('reports.urls')),
    url(r'^data/', include('data.urls')),
    url(r'^api/', include('rest.urls')),
    url(r'^reports/internal/new_users/',  new_users_report, name='new_users_report'),
    url(r'^test/',  test_report, name='test_report'),
    url(r'^email/validate/(?P<user_encode>.+)/',  validate, name='test_report'),
    (r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^statistics/exercise/', exercise_history, name='exercise_history'),
    url(r'^statistics/miles/', miles_history, name='miles_history'),
    url(r'^statistics/physical-activity-steps-this-week-distribution/', report_global_physical_steps, name='report_global_physical_steps'),
    url(r'^statistics/physical-activity-steps-distribution/', report_global_physical_steps, name='report_global_physical_steps'),
    url(r'^statistics/physical-activity-steps/', report_global_physical_steps, name='report_global_physical_steps'),
    
    url(r'^statistics/physical-activity-miles-this-week-distribution/', report_global_physical_miles, name='report_global_physical_miles'),
    url(r'^statistics/physical-activity-miles-distribution/', report_global_physical_miles, name='report_global_physical_miles'),
    url(r'^statistics/physical-activity-miles/', report_global_physical_miles, name='report_global_physical_miles'),

    url(r'^statistics/physical-activity-hours-this-week-distribution/', report_global_physical_duration, name='report_global_physical_hours'),
    url(r'^statistics/physical-activity-hours-distribution/', report_global_physical_duration, name='report_global_physical_hours'),
    url(r'^statistics/physical-activity-hours/', report_global_physical_duration, name='report_global_physical_hours'),

    url(r'^statistics/social-education-level-distribution/', report_global_social_education, name='report_global_social_education'),
    url(r'^statistics/social-education-level/', report_global_social_education, name='report_global_social_education'),
    url(r'^statistics/social-education/', report_global_social_education, name='report_global_social_education'),

    url(r'^statistics/social-work-experience-years/', report_global_social_work, name='report_global_social_work'),
    url(r'^statistics/social-work-years/', report_global_social_work, name='report_global_social_work'),
    url(r'^statistics/social-work/', report_global_social_work, name='report_global_social_work'),
    
    url(r'^statistics/social-health-conditions-distribution/', report_global_health_condition, name='report_global_health_condition'),
    url(r'^statistics/social-health-conditions/', report_global_health_condition, name='report_global_health_condition'),

    url(r'^statistics/social-health-complaints-distribution/', report_global_health_complaints, name='report_global_health_condition'),
    url(r'^statistics/social-health-complaints/', report_global_health_complaints, name='report_global_health_condition'),

    url(r'^statistics/social-health-emotions-distribution/', report_global_health_emotions, name='report_global_health_emotions'),
    url(r'^statistics/social-health-emotions/', report_global_health_emotions, name='report_global_health_emotions'),
    
    url(r'^researchkit_backend/',  datadonors_researchkit_backend, name='datadonors_researchkit_backend'),
    url(r'^researchkit_backend/doc/',  datadonors_researchkit_backend_doc, name='datadonors_researchkit_backend_doc'),
    
    url(r'^stats/miles/', get_miles, name='get_miles'),
    
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)