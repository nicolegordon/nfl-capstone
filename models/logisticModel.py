#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:48:01 2023

@author: nicolegordon
"""

import pandas as pd
import numpy as np
import os
from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.model_selection import cross_val_score

# Read in the cleaned data
X_train_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 'data', 'X_train.csv'))
X_test_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                           '..', 'data', 'X_test.csv'))
y_train_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 'data', 'y_train.csv'))
y_test_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                           '..', 'data', 'y_test.csv'))

X_train = pd.read_csv(X_train_path, index_col=0)
y_train = np.ravel(pd.read_csv(y_train_path, index_col=0))
X_test = pd.read_csv(X_test_path, index_col=0)
y_test = np.ravel(pd.read_csv(y_test_path, index_col=0))

log_reg = LogisticRegression()
log_reg.fit(X_train, y_train)

print('Training Accuracy: ', log_reg.score(X_train, y_train))
print('cross val score', cross_val_score(log_reg, X_train, y_train, 
                                         cv=10, scoring='accuracy'))
model_file = 'log_model.pkl'
pickle.dump(log_reg, open(model_file, 'wb'))