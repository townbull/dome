from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.Selector, name='selector'),
    url(r'^dropbox/$', views.DropboxChooser, name='dropbox_chooser'),
    url(r'^google/$', views.GooglePicker, name='google_picker'),
    url(r'^dropbox/save$', views.SaveInfoDropbox, name='saveInfo_dropbox'),
    url(r'^showlist$', views.Showlist, name='showlist')
)