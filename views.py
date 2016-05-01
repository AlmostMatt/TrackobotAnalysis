from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, Http404
from django.core.exceptions import PermissionDenied
from django.utils import timezone
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response

import json

import analysis

# TODO: use http://hearthstoneapi.com/ to get card text/names/images
# and use the internal card names

def decks(request):
    min_games = int(request.GET.get('min_games', 10))
    decks = analysis.load_decks(min_games=min_games)
    return render_to_response('decks.html',
            {'decks': decks})
    
def analyze(request):
    deck = request.GET.get('deck', 'UNKNOWN')
    
    results = analysis.card_analysis(deckname=deck, pages=3)
    # Sort by cost then winrate
    print(results)
    return render_to_response('analysis.html',
            {'deck': deck, 'results': results})

