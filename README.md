# TrackobotAnalysis
Card winrate analysis using Trackobot API

You can see the web version at http://almostmatt.com/dj/hearth/decks

# Local Usage
* update your Username, Password, and API Key in config.py
* Uncomment interactive_mode at the bottom of analysis.py
* $ python analysis.py
* follow instructions

# Modes
Card Analysis: For each card in a deck, find the winrate of games in which the card was played.  
Mulligan Analysis: For each matchup, find the winrate of cards played in the first 6 turns.  
Problematic Cards: For each matchup, find cards against which you have < 45% winrate.  
Short Games: Card analysis for games that last <= 9 turns.  
Long Games: Card analysis for games that last >= 15 turns.  
Time Analysis: For each hour of the day, your overall winrate.

# Config
You can find your Username and API key (token) at https://trackobot.com/profile/settings/api

You can find your Username and Password by right clicking on trackobot in the system tray and choosing 'Export'. The resulting file will contain username, password, and a link to trackbot.com.  
(Ignore any spaces or NULL characters that may appear between letters in the output file)
