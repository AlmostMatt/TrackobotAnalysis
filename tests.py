from django.test import TestCase, Client
from TrackobotAnalysis.views import *
import TrackobotAnalysis.views

from django.core.urlresolvers import reverse

import json

class SanityTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_server_info(self):
        params = {'deck': 'Mono Spells'}
        url = reverse('TrackobotAnalysis.views.analyze')
        print(url)
        response = self.client.get(reverse('TrackobotAnalysis.views.analyze'), params)
        assert response.status_code == 200, 'Status code %s' % response.status_code
        data = json.loads(response.content)
        assert data['cards']


