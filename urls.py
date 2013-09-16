from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from social.views import home, donate, logout, wizard, error, form, form2, close_login_popup, greg, comming, mock, wikilife_push, wikilife_pull
from social.facebook import facebook_view

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'google7d1bd3580ebd5b1b.html$', greg, name='greg'),
    url(r'^donate/$', donate, name='donate'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^maqueta/$', mock, name='maqueta'),
    url(r'^wizard/$', wizard, name='wizard'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^comming/', comming, name='comming'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'', include('social_auth.urls')),
    url(r'^wikilife/push', wikilife_push, name='wikilife_push'),
    url(r'^wikilife/pull', wikilife_pull, name='wikilife_pull'),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)