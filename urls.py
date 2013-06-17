try:
    from django.conf.urls import include, patterns, url
except ImportError:
    from django.conf.urls.defaults import include, patterns, url
from django.conf import settings
# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
                       # facebook and registration urls
                       (r'^facebook/', include('django_facebook.urls')),
                       #(r'^accounts/', include('django_facebook.auth_urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                        (r'^admin/', include(admin.site.urls)),
                       )

dev_patterns = patterns('connect.facebook_views',
                        url(r'^/', 'home', name='home'),
                        url(
                            r'^lazy_decorator_example/$', 'lazy_decorator_example',
                        name='facebook_lazy_decorator_example'),
                        url(r'^decorator_example/$', 'decorator_example',
                            name='facebook_decorator_example'),
                        url(
                            r'^decorator_example_scope/$', 'decorator_example_scope',
                            name='facebook_decorator_example_scope'),
                        url(r'^wall_post/$',
                            'wall_post', name='facebook_wall_post'),
                        url(r'^checkins/$',
                            'checkins', name='facebook_checkins'),
                        url(r'^image_upload/$',
                            'image_upload', name='facebook_image_upload'),
                        url(r'^canvas/$', 'canvas', name='facebook_canvas'),
                        url(r'^page_tab/$',
                            'page_tab', name='facebook_page_tab'),
                        url(r'^open_graph_beta/$', 'open_graph_beta',
                            name='facebook_open_graph_beta'),
                        url(r'^remove_og_share/$', 'remove_og_share',
                            name='facebook_remove_og_share'),
                        )

urlpatterns += dev_patterns

print settings.MODE
if settings.MODE == 'userena':
    urlpatterns += patterns('',
                            (r'^accounts/', include('userena.urls')),
                            )
elif settings.MODE == 'django_registration':
    urlpatterns += patterns('',
                            (r'^accounts/', include(
                                'registration.backends.default.urls')),
                            )


if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
                                'document_root': settings.MEDIA_ROOT,
                                }),
                            )
