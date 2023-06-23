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
from sklearn.neighbors import KNeighborsClassifier
import pickle
from sklearn.metrics import mean_squared_error

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

param_grid = {'n_neighbors': [65, 75, 85]}
ref_knn = GridSearchCV(KNeighborsClassifier(), 
                          param_grid=param_grid, 
                          verbose=1, 
                          cv=3)
ref_knn.fit(X_train, y_train)

print("The best refined KNN Classifier parameters are: ", ref_knn.best_params_)

knn_params = ref_knn.best_params_
knn_clf_opt = KNeighborsClassifier(n_neighbors=knn_params['n_neighbors'])
knn_clf_opt.fit(X_train, y_train)

def get_mse(model, model_name):
    mse = round(mean_squared_error(y_test, model.predict(X_test)), 4)
    print(f'{model_name} MSE: {mse}')
    
get_mse(knn_clf_opt, "KNN Classifier")

model_file = 'knn_model.pkl'
pickle.dump(ref_knn, open(model_file, 'wb'))