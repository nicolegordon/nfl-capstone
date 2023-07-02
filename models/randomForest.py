#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 20:48:01 2023

@author: nicolegordon
"""

import pandas as pd
import numpy as np
import os
from sklearn.model_selection import GridSearchCV
from sklearn.ensemble import RandomForestClassifier
import pickle
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
param_grid = {'max_depth': [38, 40],
             'n_estimators': [100, 110],
             'min_samples_split': [10, 12]}
ref_rand = GridSearchCV(RandomForestClassifier(), 
                          param_grid=param_grid, 
                          verbose=1, 
                          cv=5)
ref_rand.fit(X_train, y_train)

print("The best refined Random Forest Classifier parameters are: ", 
      ref_rand.best_params_)
#%%
# Optimal model
rnd_params = ref_rand.best_params_
# rnd_params = {'max_depth': 38, 'min_samples_split': 10, 'n_estimators': 110}
rnd_clf_opt = RandomForestClassifier(min_samples_split=rnd_params['min_samples_split'],
                                    max_depth=rnd_params['max_depth'],
                                    n_estimators=rnd_params['n_estimators'])
rnd_clf_opt.fit(X_train, y_train)

# Compute accuracy of model
def get_acc(model, model_name):
    accuracy = round(accuracy_score(y_test, model.predict(X_test)), 4)
    print(f'{model_name} Accuracy: {accuracy}')
    acc_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            'rf_acc.txt'))
    with open(acc_file, 'w') as f:
        f.write(f'{model_name} Accuracy: {accuracy}')
    
get_acc(rnd_clf_opt, "Random Forest Classifier")

# Export model
model_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                          'rf_model.pkl'))
pickle.dump(ref_rand, open(model_file, 'wb'))