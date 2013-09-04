from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from social.views import home, donate, logout, error, form, form2, close_login_popup, greg, comming,receive_code
from social.facebook import facebook_view

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'google7d1bd3580ebd5b1b.html$', greg, name='greg'),
    url(r'^donate/$', donate, name='donate'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^receive_code/', receive_code, name='receive_code'),
    url(r'^comming/', comming, name='comming'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'', include('social_auth.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
