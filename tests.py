from django.test import TestCase, Client
from TrackobotAnalysis.views import *
import TrackobotAnalysis.views

from django.core.urlresolvers import reverse

import json

class SanityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_response_ok(self):
        params = {'deck': 'Mono Spells'}
        url = reverse('TrackobotAnalysis.views.analyze')
        print(url)
        response = self.client.get(reverse('TrackobotAnalysis.views.analyze'), params)
        response = self.client.get(reverse('TrackobotAnalysis.views.decks'), params)
        assert response.status_code == 200, 'Status code %s' % response.status_code


