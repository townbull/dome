from django.conf.urls import patterns, include, url
import views


urlpatterns = patterns('',
    url(r'^login/$', views.login_view, name="login"),
    url(r'^logout/$', views.logout_view, name="logout"),
    url(r'', include('social.apps.django_app.urls', namespace='social'))
)