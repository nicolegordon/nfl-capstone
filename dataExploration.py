#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 21 08:39:23 2023

@author: nicolegordon
"""

import pandas as pd
import numpy as np
import os

# Download data from Github
years = np.arange(2009, 2020)

pbpCols = ['play_id', 'game_id', 'home_team', 'away_team', 'posteam', 
        'posteam_type', 'defteam', 'side_of_field', 'yardline_100', 
        'game_date', 'quarter_seconds_remaining', 'half_seconds_remaining', 
        'game_seconds_remaining', 'game_half', 'quarter_end', 'drive', 'sp', 
        'qtr', 'down', 'goal_to_go', 'time', 'yrdln', 'ydstogo',
        'total_home_score', 'total_away_score', 'score_differential']
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
                          
    pbpData = pd.concat([pbpData, pbpDf], ignore_index=True)
    gamesData = pd.concat([gamesData, gamesDf], ignore_index=True)
    del regSeasonPbpUrl, regSeasonGamesUrl, pbpDf, gamesDf

# Clean up variables
del year, years, pbpCols, gamesCols

# Drop plays where the down is undefined
# These are beginning/half time/end, 2 min warnings, timeouts, kickoffs
pbpData = pbpData[~pbpData.down.isna()]

# Drop plays where there is no defined possesion team
pbpData = pbpData[~pbpData.posteam.isna()]

# Drop columns that provide redundant or no information
pbpData = pbpData.drop(columns=['play_id', 'game_date', 'side_of_field', 
                                'yrdln', 'time', 'goal_to_go', 'sp',
                                'posteam', 'defteam', 'quarter_end'])
gamesData = gamesData.drop(columns=['season'])

# Join the gamesData to the pbpData
data = pbpData.merge(gamesData, 'inner').reset_index(drop=True)
del pbpData, gamesData

# Preprocess data
# Need to split and stack data so there is one team per row
homeDf = data.copy().drop(columns=['home_team', 'away_team'])
homeDf.home_team = 1
homeDf['has_posession'] = (homeDf.posteam_type == 'home').astype(int)
homeDf = homeDf.rename(columns={'total_home_score': 'cur_score',
                                'total_away_score': 'opp_cur_score',
                                'home_score': 'final_score',
                                'away_score': 'opp_final_score'})
homeDf['won'] = (homeDf.final_score > homeDf.opp_final_score).astype(int)
homeDf.score_differential = homeDf.cur_score - homeDf.opp_cur_score
homeDf = homeDf.drop(columns=['posteam_type'])

awayDf = data.copy().drop(columns=['home_team', 'away_team'])
awayDf.home_team = 0
awayDf['has_posession'] = (awayDf.posteam_type != 'home').astype(int)
awayDf = awayDf.rename(columns={'total_away_score': 'cur_score',
                                'total_home_score': 'opp_cur_score',
                                'away_score': 'final_score',
                                'home_score': 'opp_final_score'})
awayDf['won'] = (awayDf.final_score > awayDf.opp_final_score).astype(int)
awayDf.score_differential = awayDf.cur_score - awayDf.opp_cur_score
awayDf = awayDf.drop(columns=['posteam_type'])

data = (pd.concat((homeDf, awayDf), ignore_index=True)
        .sort_values(['game_id'], ignore_index=True))
del homeDf, awayDf

# One-hot encode game_half
game_half = pd.get_dummies(data.game_half)
data = pd.concat((data.drop(columns=['game_half']), game_half), axis=1)
del game_half

# Write cleaned data to csv
wdir = r'/Users/nicolegordon/Documents/DS/Capstone'
data.to_csv(os.path.join(wdir, 'cleanData.csv'), index=False)