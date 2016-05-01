from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^decks/$', 'TrackobotAnalysis.views.decks'),
    url(r'^analyze/$', 'TrackobotAnalysis.views.analyze'),
)
