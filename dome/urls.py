from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^$', views.Selector, name='selector'),
    #url(r'^dropbox/$', views.DropboxChooser, name='dropbox_chooser'),
    #url(r'^google/$', views.GooglePicker, name='google_picker'),
    url(r'^dropbox/save$', views.SaveInfoDropbox, name='saveInfo_dropbox'),
    url(r'^googleDrive/save$', views.SaveInfoGoogle, name='saveInfo_google'),
    url(r'^showlist$', views.Showlist, name='showlist'),
    url(r'^gettoken$', views.GetToken, name='gettoken'),
    url(r'^getaccinfo$', views.GetAccInfo, name='getaccinfo'),
    # url(r'^$', views.authredirect, name='authredirect'),
    # url(r'^gdrive/$', views.IndexView.as_view(), name='index'),
)