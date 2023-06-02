#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:48:01 2023

@author: nicolegordon
"""

import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.model_selection import cross_val_score

# Read in the cleaned data
wdir = r'/Users/nicolegordon/Documents/DS/Capstone'
data = pd.read_csv(os.path.join(wdir, 'cleanData.csv'))
data = data.drop(columns=['game_id', 'final_score', 'opp_final_score'])

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
# variable (<0.01)
win_corr = data.corr()['won'].sort_values(ascending=False)
win_corr_drop = win_corr[(win_corr.abs() < 0.01)]
data = data.drop(columns=win_corr_drop.index.to_list())

# Split the data into a training set and a test set
X = data.drop(columns=['won'])
y = data.won.copy()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Scale the data
pipeline = Pipeline([('std_scaler', StandardScaler())
                     ])
X_train_transformed = pd.DataFrame(pipeline.fit_transform(X_train),
                                   columns=X_train.columns)

log_reg = LogisticRegression()
log_reg.fit(X_train_transformed, y_train)

print('Training Accuracy: ', log_reg.score(X_train, y_train))
print('cross val score', cross_val_score(log_reg, X_train, y_train, 
                                         cv=10, scoring='accuracy'))
