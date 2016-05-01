from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required

import json


def analyze(request):
    response_data = {
        'cards': [
            ('The Coin', 30),
            ('Flash Heal', 80),
            ('Ysera', 100),
        ]
    }
    return HttpResponse(json.dumps(response_data), content_type="application/json")

