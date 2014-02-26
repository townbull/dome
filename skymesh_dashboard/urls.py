from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic.base import RedirectView

admin.autodiscover()

urlpatterns = patterns('',
    # prevent the extra are-you-sure-you-want-to-logout step on logout
    #(r'^accounts/logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}),

    url(r'^accounts/', include('allauth.urls')),
    url(r'^console/', include('dome.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', RedirectView.as_view(url='/console/', permanent=False), name='index'),

)