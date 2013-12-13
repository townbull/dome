from django.conf.urls import patterns, url

from .views import IndexView, authredirect

urlpatterns = patterns('',
    url(r'^$', authredirect, name='authredirect'),
    url(r'^gdrive/$', IndexView.as_view(), name='index'),
)