from django.conf.urls import patterns, include, url
import views
from allauth.account.views import LogoutView


urlpatterns = patterns('',
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', LogoutView.as_view(), name="logout"),
)