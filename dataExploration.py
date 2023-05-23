#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 08:39:23 2023

@author: nicolegordon
"""

import pandas as pd
import numpy as np

years = np.arange(2009, 2020)

pbpCols = ['play_id', 'game_id', 'home_team', 'away_team', 'posteam', 
        'posteam_type', 'defteam', 'side_of_field', 'yardline_100', 
        'game_date', 'quarter_seconds_remaining', 'half_seconds_remaining', 
        'game_seconds_remaining', 'game_half', 'quarter_end', 'drive', 'sp', 
        'qtr', 'down', 'goal_to_go', 'time', 'yrdln', 'ydstogo',
        'total_home_score', 'total_away_score', 'posteam_score',
        'defteam_score', 'score_differential']
gamesCols = ['game_id',	'home_team', 'away_team', 'week', 
              'season',	'home_score', 'away_score']

pbpData = pd.DataFrame(columns=pbpCols)
gamesData = pd.DataFrame(columns=gamesCols)

for year in years:
    regSeasonPbpUrl = ('https://github.com/ryurko/nflscrapR-data'
                        + '/raw/master/play_by_play_data/regular_season'
                        + f'/reg_pbp_{year}.csv')
    regSeasonGamesUrl = ('https://github.com/ryurko/nflscrapR-data/raw/'
                          + 'master/games_data/regular_season'
                          + f'/reg_games_{year}.csv')
    
    pbpDf = pd.read_csv(regSeasonPbpUrl, header=0, usecols=pbpCols)
    gamesDf = pd.read_csv(regSeasonGamesUrl, header=0, usecols=gamesCols)
                          
    pbpData = pd.concat([pbpData, pbpDf])
    gamesData = pd.concat([gamesData, gamesDf])

