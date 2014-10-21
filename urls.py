from django.contrib import admin
admin.autodiscover()

from django.conf import settings
from django.conf.urls import patterns, include, url
#from social.facebook import facebook_view
from views import *
from reports.views import *

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
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
    
    url(r'^statistics/physical-activity-steps-this-week-distribution/', report_global_physical_steps, name='report_global_physical_steps'),
    url(r'^statistics/physical-activity-steps-distribution/', report_global_physical_steps, name='report_global_physical_steps'),
    url(r'^statistics/physical-activity-steps/', report_global_physical_steps, name='report_global_physical_steps'),
    
    url(r'^statistics/physical-activity-miles-this-week-distribution/', report_global_physical_miles, name='report_global_physical_miles'),
    url(r'^statistics/physical-activity-miles-distribution/', report_global_physical_miles, name='report_global_physical_miles'),
    url(r'^statistics/physical-activity-miles/', report_global_physical_miles, name='report_global_physical_miles'),

    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)