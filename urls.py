from django.conf.urls import patterns, url

from TrackobotAnalysis import views

urlpatterns = patterns('',
    url(r'^analyze/$', views.analyze),
)
