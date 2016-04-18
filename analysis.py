import json
import requests
import os
import pytz
import sys

from datetime import datetime, date
from collections import defaultdict, OrderedDict
from config import USERNAME, PASSWORD, LOCAL_TZ, API_KEY

MODES = ['arena', 'ranked', 'friendly', 'casual']
CLASSES = ['Warrior', 'Warlock', 'Priest', 'Paladin', 'Mage', 'Rogue', 'Shaman', 'Hunter', 'Druid']
PAGE_SIZE = 15

HERO_POWERS = {
    'Lesser Heal', 'Life Tap', 'Shape Shift', 'Fireblast', 'Armor Up', 'Dagger Mastery',
    'Steady Shot', 'Reinforce', 'Totemic Call',
    'Heal', 'Soul Tap', 'Dire Shapeshift', 'Fireblast Rank 2', 'Tank Up', 'Poisoned Daggers',
    'Ballista Shot', 'The Silver Hand', 'Totemic Slam',
    'Mind Spike', 'Mind Shatter', 'INFERNO!', 'DIE, INSECT!', 'Lightning Jolt',
}
TOKEN_CARDS = {
    'Nightmare', 'Dream', 'Ysera Awakens', 'Emerald Drake', 'Laughing Sister',
    'Gallywix\'s Coin',
    'Armor Plating', 'Emergency Coolant', 'Finicky Cloakfield', 'Reversing Switch', 'Rusty Horn',
    'Time Rewinder', 'Whirling Blades',
    'Bananas', 'Cursed!', 'Excess Mana', 'Roaring Torch', 'Tail Swipe',
    'Map to the Golden Monkey', 'Golden Monkey',
    'Lantern of Power', 'Timepiece of Horror', 'Mirror of Doom',
}
THE_COIN = 'The Coin'

# TODO: for a given deck/matchup, give winrate for each card
# (especially the winrate if the card is places in the first 4-6 turns)
# to help with mulligans and deck tweaking

# TODO: for a given deck, card, show id/time of games that contained that crd
# so that I can cleanup trackobot

# TODO: give inputs for game mode and #pages

def clear():
    print('')
    #this is not working for me on cygwin
    #os.system('cls' if os.name == 'nt' else 'clear')

def interactive_mode():
    options = ['Card Analysis', 'Mulligan Analyis', 'Time Analysis', 'Nevermind']
    for i in range(len(options)):
        print('(%s) %s' % (i+1, options[i]))
    num = int(raw_input('Choose an analysis type: '))
    if num == 1:
        deck = choose_deck()
        card_analysis(deckname=deck, pages=None)
    elif num == 2:
        deck = choose_deck()
        mulligan_analysis(deckname=deck, pages=None)
    elif num == 3:
        time_analysis(mode=None, pages=10)

def choose_deck():
    clear()
    print('Loading decks...')
    url = ('https://trackobot.com/profile/stats/decks.json?order=desc&sort_by=share'
            '&mode=ranked&username=%s&token=%s' % (USERNAME, API_KEY))
    r = requests.get(url, auth=(USERNAME, PASSWORD))
    clear()
    # ordered dict preserves the order of the deck list
    data = json.loads(r.text, object_pairs_hook=OrderedDict)
    deck_results = data['stats']['as_deck']
    i = 1
    for deck, results in deck_results.items()[:9]:
        print_winrate('  (%s) %s' % (i, deck), results['wins'], results['losses'])
        i+=1
    num = raw_input('Choose a deck: ')
    clear()
    deck = deck_results.keys()[int(num)-1]
    print('Selected %s.' % deck)
    return deck

def num_pages(mode=None, deck=None):
    url = ("https://trackobot.com/profile/history.json?username=%s&token=%s"
            % (USERNAME, API_KEY))
    if deck is not None:
        url = url + "&query=%s" % (deck)
    elif mode is not None:
        url = url + "&query=%s" % (mode)
    r = requests.get(url, auth=(USERNAME, PASSWORD))
    data = r.json()
    total = data['meta']['total_pages']
    if total > 5:
        clear()
        print('Found ~%s games, how many do you want to load?' % (total * PAGE_SIZE))
        inpt = raw_input("Enter a number between 0 and %s or 'a' for all: " % (total * PAGE_SIZE))
        if inpt not in ['a', 'all', "'all'"]:
            total = min((int(inpt) + PAGE_SIZE - 1)/PAGE_SIZE, total)
        clear()
    return total

def load_page(page=1, mode=None, deck=None):
    url = ("https://trackobot.com/profile/history.json?page=%s&username=%s&token=%s"
            % (page, USERNAME, API_KEY))
    if deck is not None:
        url = url + "&query=%s" % (deck)
    elif mode is not None:
        url = url + "&query=%s" % (mode)
    r = requests.get(url, auth=(USERNAME, PASSWORD))
    data = r.json()
    return data['history']

def utc_to_local(utc_dt):
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(LOCAL_TZ)
    return LOCAL_TZ.normalize(local_dt) # .normalize might be unnecessary

def load_games(pages=None, mode=None, deck=None):
    if pages is None:
        pages = num_pages(mode=mode, deck=deck)
    games = []
    for page in range(1, pages+1):
        sys.stdout.write('\r')
        str = "Loading page %s/%s" % (page, pages)
        sys.stdout.write(str)
        sys.stdout.flush()
        more_games = load_page(page=page, mode=mode, deck=deck)
        if not more_games: break
        games.extend(more_games)
    print("")
    print("Loaded %s games" % len(games))
    return games

def cards_by_cost(card_cost_map):
    cost_card_map = defaultdict(list)
    tokens = []
    hero_powers = []
    for card, cost in card_cost_map.items():
        if card in TOKEN_CARDS:
            tokens.append(card)
        elif card in HERO_POWERS:
            hero_powers.append(card)
        elif card == THE_COIN:
            continue
        else:
            cost_card_map[cost].append(card)
    return ([(cost, cost_card_map[cost]) for cost in sorted(cost_card_map.keys())]
            + [('Tokens', tokens), ('Hero Powers', hero_powers)])

def print_winrate(name, w, l, suffix = ''):
    # division by 0 case
    if w + l == 0: return
    print("{:25s} {:3d}/{:<3d}  {:6s}    {}".format(name, w, l, '(%s%%)' % winrate(w,l), suffix))

def winrate(w, l):
    if w + l == 0: return 0
    return int(100*(float(w)/(w+l)))

def average(list_nums):
    return float(sum(list_nums))/len(list_nums)

def card_analysis(deckname="Mono Spells", pages=None):
    games = load_games(pages=pages, deck=deckname, mode='ranked')
    cards = set()
    card_cost = defaultdict(int)
    card_w = defaultdict(int)
    card_l = defaultdict(int)
    card_turn_played = defaultdict(list)
    card_game_duration = defaultdict(list)
    game_count = 0
    order_w = defaultdict(int)
    order_l = defaultdict(int)
    for game in games:
        if game['mode'] != 'ranked': continue
        if game['hero_deck'] != deckname: continue
        order = 'second' if game['coin'] else 'first'
        game_count += 1
        won = game['result'] == 'win'
        last_turn = game['card_history'][-1]['turn']
        if won:
            order_w[order] += 1
        else:
            order_l[order] += 1
        for entry in game['card_history']:
            turn = entry['turn']
            if entry['player'] == 'me':
                card = entry['card']['name']
                card_cost[card] = entry['card']['mana']
                card_turn_played[card].append(turn)
                card_game_duration[card].append(last_turn)
                if won:
                    card_w[card] += 1
                else:
                    card_l[card] += 1
    print("Loaded %s ranked games as %s" % (game_count, deckname))
    print('')
    print_winrate("Going First", order_w['first'], order_l['first'])
    print_winrate("Going Second", order_w['second'], order_l['second'])
    print_card_stats(THE_COIN, card_w[THE_COIN], card_l[THE_COIN],
        card_turn_played[THE_COIN], card_game_duration[THE_COIN])
    for cost, cards in cards_by_cost(card_cost):
        print('')
        print("(%s)" % cost)
        for card in sorted(cards, reverse=True, key=lambda x: winrate(card_w[x], card_l[x])):
            print_card_stats(card, card_w[card], card_l[card],
                    card_turn_played[card], card_game_duration[card])

def print_card_stats(cardname, wins, losses, turns_played=[], game_durations=[]):
    if wins + losses <= 1:
        return
    avg_turn = round(average(turns_played), 2)
    avg_duration = round(average(game_durations), 2)
    suffix = 'Turn: %s, \tDuration: %s turns.' % (avg_turn, avg_duration)
    print_winrate(cardname, wins, losses, suffix=suffix)


def mulligan_analysis(deckname="Mono Spells", pages=None):
    games = load_games(pages=pages, deck=deckname, mode='ranked')
    cards = set()
    card_cost = defaultdict(int)
    matchup_card_w = defaultdict(lambda: defaultdict(int))
    matchup_card_l = defaultdict(lambda: defaultdict(int))
    game_count = 0
    for game in games:
        if game['mode'] != 'ranked': continue
        if game['hero_deck'] != deckname: continue
        game_count += 1
        opp = game['opponent']
        won = game['result'] == 'win'
        for entry in game['card_history']:
            turn = entry['turn']
            if turn > 6: continue
            if entry['player'] == 'me':
                card = entry['card']['name']
                if card in HERO_POWERS or card in TOKEN_CARDS: continue
                card_cost[card] = entry['card']['mana']
                if won:
                    matchup_card_w[opp][card] += 1
                else:
                    matchup_card_l[opp][card] += 1
    print("Loaded %s ranked games as %s" % (game_count, deckname))
    for hero in CLASSES:
        print("")
        print("%s vs %s" % (deckname, hero))
        for cost, cards in cards_by_cost(card_cost):
            #print("")
            #print("(%s)" % cost)
            for card in sorted(cards, reverse=True,
                    key=lambda x: winrate(matchup_card_w[hero][x], matchup_card_l[hero][x])):
                print_winrate(card, matchup_card_w[hero][card], matchup_card_l[hero][card])

# analyzes winrate for a given hour
def time_analysis(mode=None, pages=None):
    games = load_games(mode=mode, pages=pages)
    hours = range(24)
    wins = {hour:0 for hour in hours}
    losses = {hour:0 for hour in hours}
    for game in games:
        mode = game['mode']
        hero = game['hero']
        deck = game['hero_deck']
        opp = game['opponent']
        oppdeck = game['opponent_deck']
        order = 'second' if game['coin'] else 'first'
        result = game['result'] # win or loss
        duration = game['duration'] # int, second
        card_history = game['card_history']
        if mode == 'ranked':
            rank = game['rank'] # int
        timestring = game['added'] # 'yyyy-mm-ddThh:mm:ss.zzzZ'
        dt = utc_to_local(datetime.strptime(timestring[:-5], "%Y-%m-%dT%H:%M:%S"))
        time = dt.time()
        if result == 'win':
            wins[time.hour] += 1
        else:
            losses[time.hour] += 1
    for hour in hours:
        w = wins[hour]
        l = losses[hour]
        if (w+l) > 0:
            print_winrate('%sh' % hour, w, l)

interactive_mode()
