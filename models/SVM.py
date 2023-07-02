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
from sklearn.svm import SVC
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

# Scale the data for SVM
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Grid seach for hyperparamters
param_grid = {'kernel': ['linear', 'rbf'],
              'C': [1e2, 1e6, 1e10]}
ref_svm = GridSearchCV(SVC(), 
                        param_grid=param_grid, 
                        verbose=1, 
                        cv=3)
ref_svm.fit(X_train, y_train)

print("The best refined SVM parameters are: ", ref_svm.best_params_)
### STOP HERE
### Too much data for an SVM
#%%
# Optimal model
svm_params = ref_svm.best_params_
svm_clf_opt = SVC(n_neighbors=svm_params['n_neighbors'])
svm_clf_opt.fit(X_train, y_train)

# Compute accuracy of model
def get_acc(model, model_name):
    accuracy = round(accuracy_score(y_test, model.predict(X_test)), 4)
    print(f'{model_name} Accuracy: {accuracy}')
    
get_acc(svm_clf_opt, "SVM")

# Export model
model_file = 'svm_model.pkl'
pickle.dump(ref_svm, open(model_file, 'wb'))