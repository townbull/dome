from django.conf.urls import patterns, url
import views


urlpatterns = patterns('',
    url(r'^login/$', views.login_user, name="login"),
)