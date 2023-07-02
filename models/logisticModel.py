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
# from sklearn.model_selection import cross_val_score
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score

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

# Grid seach for hyperparamters
param_grid = {'C': np.arange(0.1, 0.35, 0.05),
              'solver': ['newton-cg', 'linear']}
ref_log = GridSearchCV(LogisticRegression(), 
                          param_grid=param_grid, 
                          verbose=1, 
                          cv=3) 
ref_log.fit(X_train, y_train)

print("The best refined Logistic Regression parameters are: ", ref_log.best_params_)
#%%
# Optimal model
log_params = ref_log.best_params_
# log_params = {'C': 0.15, 'solver': 'newton-cg'}
log_reg_opt = LogisticRegression(C=log_params['C'], solver=log_params['solver'])
log_reg_opt.fit(X_train, y_train)

# Compute accuracy of model
def get_acc(model, model_name):
    accuracy = round(accuracy_score(y_test, model.predict(X_test)), 4)
    print(f'{model_name} Accuracy: {accuracy}')
    acc_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'log_acc.txt'))
    with open(acc_file, 'w') as f:
        f.write(f'{model_name} Accuracy: {accuracy}')

get_acc(log_reg_opt, "Logistic Regression")

# Export model
model_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                          'log_model.pkl'))
pickle.dump(log_reg_opt, open(model_file, 'wb'))