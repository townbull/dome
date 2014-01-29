from django.conf.urls import patterns, include, url


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'skymesh_dashboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/$', include(admin.site.urls)),
    url(r'^auth/', include('acorn.urls')),
    url(r'^selector/', include('kiwi.urls')),
    url(r'^', include('dome.urls')),
)