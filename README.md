# TrackobotAnalysis
Card winrate analysis using Trackobot API

# Usage
* update your Username, Password, and API Key in config.py
* $ python analysis.py
* follow instructions

# Modes
Card Analysis: For each card in a deck, find the winrate of games in which the card was played.
Mulligan Analysis: For each matchup, find the winrate of cards played in the first 6 turns.  
Time Analysis: For each hour of the day, your overall winrate.

# Config
You can find your Username and API key (token) at https://trackobot.com/profile/settings/api

You can find your Username and Password by right clicking on trackobot in the system tray and choosing 'Export'. The resulting file will contain username, password, and a link to trackbot.com.  
(Ignore any spaces or NULL characters that may appear between letters in the output file)
