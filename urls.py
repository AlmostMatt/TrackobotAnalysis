from django.conf.urls import patterns, url

from TrackobotAnalysis import views

urlpatterns = patterns('',
    url(r'^decks/$', views.decks),
    url(r'^analyze/$', views.analyze),
)
