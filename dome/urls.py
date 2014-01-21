from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.authredirect, name='authredirect'),
    url(r'^gdrive/$', views.IndexView.as_view(), name='index'),
)