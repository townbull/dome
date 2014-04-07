from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',

    #url(r'^dropbox/$', views.DropboxChooser, name='dropbox_chooser'),
    #url(r'^google/$', views.GooglePicker, name='google_picker'),
    # url(r'^dropbox/save$', views.SaveInfoDropbox, name='saveInfo_dropbox'),
    # url(r'^googleDrive/save$', views.SaveInfoGoogle, name='saveInfo_google'),

    #url(r'^addcloud/$', views.addCloud, name='addcloud'),
    url(r'^showlist$', views.Showlist, name='showlist'),
    url(r'^$', views.Selector, name='selector'),
)