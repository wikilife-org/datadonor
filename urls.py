from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin
from django.conf import settings

from social.views import home, done, logout, error, form, form2, close_login_popup
from social.facebook import facebook_view
from social.vkontakte import vkontakte_view
from social.odnoklassniki import ok_app, ok_app_info

admin.autodiscover()


urlpatterns = patterns('',
    url(r'^$', home, name='home'),
    url(r'google7d1bd3580ebd5b1b.html$', greg, name='greg'),
    url(r'^done/$', done, name='done'),
    url(r'^error/$', error, name='error'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^form/$', form, name='form'),
    url(r'^form2/$', form2, name='form2'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^fb/', facebook_view, name='fb_app'),
    url(r'^vk/', vkontakte_view, name='vk_app'),
    url(r'^ok/$', ok_app, name='ok_app'),
    url(r'^ok/info/$', ok_app_info, name='ok_app_info'),
    url(r'^close_login_popup/$', close_login_popup, name='login_popup_close'),
    url(r'', include('social_auth.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
)
