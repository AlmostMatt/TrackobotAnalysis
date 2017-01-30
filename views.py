from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt

import analysis
import json

# TODO: use http://hearthstoneapi.com/ to get card text/names/images
# and use the internal card names

def decks(request):
    username = request.GET.get('username', None)
    token = request.GET.get('token', None)
    min_games = int(request.GET.get('min_games', 10))
    decks = analysis.load_decks(username=username, token=token, min_games=min_games)
    return render_to_response('hearth/decks.html',
            {'decks': decks})

def analyze(request):
    username = request.GET.get('username', None)
    token = request.GET.get('token', None)
    deck = request.GET.get('deck', 'UNKNOWN')
    games = int(request.GET.get('games', 40))

    results = analysis.card_analysis(username=username, token=token, deckname=deck, num_games=games)
    # Sort by cost then winrate
    return render_to_response('hearth/analysis.html',
            {'deck': deck, 'results': results})

