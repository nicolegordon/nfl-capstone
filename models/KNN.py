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
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler

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

# Scale the data for KNN
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Grid seach for hyperparamters
param_grid = {'n_neighbors': [4, 5, 6, 7, 8]}
ref_knn = GridSearchCV(KNeighborsClassifier(), 
                          param_grid=param_grid, 
                          verbose=1, 
                          cv=5)
ref_knn.fit(X_train, y_train)

print("The best refined KNN Classifier parameters are: ", ref_knn.best_params_)
#%%
# Optimal model
knn_params = ref_knn.best_params_
# knn_params = {'n_neighbors': 7}
knn_clf_opt = KNeighborsClassifier(n_neighbors=knn_params['n_neighbors'])
knn_clf_opt.fit(X_train, y_train)

# Compute accuracy of model
def get_acc(model, model_name):
    accuracy = round(accuracy_score(y_test, model.predict(X_test)), 4)
    print(f'{model_name} Accuracy: {accuracy}')
    acc_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'knn_acc.txt'))
    with open(acc_file, 'w') as f:
        f.write(f'{model_name} Accuracy: {accuracy}')
        
    
get_acc(knn_clf_opt, "KNN Classifier")

# Export model
model_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                          'knn_model.pkl'))
pickle.dump(ref_knn, open(model_file, 'wb'))