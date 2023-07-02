#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 22 21:42:13 2023

@author: nicolegordon
"""

import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.model_selection import train_test_split

# Read in the cleaned data
data_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                         'cleanData.csv'))
data = pd.read_csv(data_file)
data = data.drop(columns=['game_id', 'final_home_score', 'final_away_score'])

# Check correlations between variables
def corrMat(data):
    plt.figure(figsize=(10,7))
    mask = np.triu(np.ones_like(data.corr(), dtype=bool))
    sns.heatmap(data.corr(), annot=True, mask=mask, vmin=-1, vmax=1)
    plt.title('Correlation Coefficient Of Predictors')
    plt.show()
# Iniitial correlation matrix
corrMat(data)
# Drop predictors that are highly correlated with each other (>0.8)
data = data.drop(columns=['Half1', 'Half2', 'game_seconds_remaining', 
                          'drive'])
corrMat(data)
# Drop predictors that have extremely low correlation with the target 
# variable (<0.005)
win_corr = data.corr()['home_won'].sort_values(ascending=False)
win_corr_drop = win_corr[(win_corr.abs() < 0.005)]
data = data.drop(columns=win_corr_drop.index.to_list())
# Drop half_seconds_remaining and Overtime
# as these would be highly correlated with qtr 
data = data.drop(columns=['Overtime', 'half_seconds_remaining'])

# Split the data into a training set and a test set
X = data.drop(columns=['home_won'])
y = data.home_won.copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Write data to csv files
X_train.to_csv('X_train.csv', index=True)
X_test.to_csv('X_test.csv', index=True)
y_train.to_csv('y_train.csv', index=True)
y_test.to_csv('y_test.csv', index=True)