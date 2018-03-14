"""
 # Data Structures and Algorithms - Part B
 # Created by Reece Benson (16021424)
"""
# Imports
import json
import pickle
from os import system as call
from functools import partial
from tennis import Season
from tennis.File import File
from tennis.Menu import Builder

# Variables
gamePath = "./data/json/game.json"
sessionPath = "./data/pickle/session.pickle"
settingsPath = "./data/json/settings.json"
playersPath = "./data/json/players.json"
rankingPointsPath = "./data/json/rankingPoints.json"

class Game():
    game = None
    parent = None
    debug = True
    seasons = None
    settings = None

    def __init__(self, _parent):
        # Initial Variables
        self.game = self
        self.parent = _parent
        self.seasons = { }
        self.settings = { }

    def load(self, mode):
        # Load Settings
        with open(settingsPath) as settings_file:
            self.settings = json.load(settings_file)

        # Load New Data
        if(mode == "new"):
            # Transfer original data
            with open(sessionPath, 'wb') as session_file:
                with open(gamePath) as game_file:
                    game_data = json.load(game_file)
                    seasons = game_data["seasons"]

                    for season in seasons:
                        # Load our Season in (if it is new)
                        if(season not in self.seasons):
                            # Get our Players
                            season_players = None
                            with open(playersPath) as players_file:
                                season_players = json.load(players_file)

                            # Create our Season Object
                            new_season = Season.Season(self.game, season, seasons[season], season_players)

                            # Update our Seasons List
                            self.seasons.update({ season: new_season })
                
                # Save Session
                pickle.dump(self.seasons, session_file, protocol=pickle.HIGHEST_PROTOCOL)

        # Load Previous Data
        elif(mode == "previous"):
            with open(sessionPath, 'rb') as session_file:
                self.seasons = pickle.load(session_file)

    def clear_screen(self):
        call("cls")

    def exit(self):
        # Save current session
        print("Saving session...")
        File().save_session(self.seasons)
        print("done.")

        # Exit
        self.parent.exit()
