from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.Selector, name='selector'),
    url(r'^dropbox/$', views.DropboxChooser, name='dropbox_chooser'),
    url(r'^google/$', views.GooglePicker, name='google_picker')
)