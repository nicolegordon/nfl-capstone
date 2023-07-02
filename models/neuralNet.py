#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun 26 17:32:49 2023

@author: nicolegordon
"""
import pandas as pd
import numpy as np
import os
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import pickle
from tensorflow import keras
from scikeras.wrappers import KerasClassifier
from scipy.stats import reciprocal
from sklearn.model_selection import RandomizedSearchCV

# Read in the cleaned data
X_train_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 'data', 'X_train.csv'))
X_test_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                           '..', 'data', 'X_test.csv'))
y_train_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                            '..', 'data', 'y_train.csv'))
y_test_path = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                           '..', 'data', 'y_test.csv'))

X_train_full = pd.read_csv(X_train_path, index_col=0)
y_train_full = np.ravel(pd.read_csv(y_train_path, index_col=0))
X_test = pd.read_csv(X_test_path, index_col=0)
y_test = np.ravel(pd.read_csv(y_test_path, index_col=0))

X_train, X_valid, y_train, y_valid = train_test_split(X_train_full, 
                                                      y_train_full)

# Scale the data for Nearual Net
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_valid = scaler.transform(X_valid)
X_test = scaler.transform(X_test)


# Build model
def build_model(n_hidden=1, n_neurons=30, learning_rate=3e-3, 
                input_shape=[X_train.shape[1]]):
    model = keras.models.Sequential()
    model.add(keras.layers.Flatten(input_shape=input_shape))
    for layer in range(n_hidden):
        model.add(keras.layers.Dense(n_neurons, activation="relu"))
    model.add(keras.layers.Dense(1, activation='sigmoid'))
    optimizer = keras.optimizers.SGD(learning_rate=learning_rate)
    model.compile(loss="binary_crossentropy", 
                  optimizer=optimizer, 
                  metrics=['accuracy'])
    return model

keras_clf = KerasClassifier(build_model, n_hidden=0, 
                            n_neurons=1, learning_rate=0.0006665773642619745)

# Grid seach for hyperparamters
param_distribs = {
    'n_hidden': (0, 1, 2, 3),
    'n_neurons': np.arange(10, 75, 10),
    'learning_rate': reciprocal(3e-4, 3e-2)
}

rnd_search_cv = RandomizedSearchCV(keras_clf, param_distribs, n_iter=3, 
                                    cv=3, verbose=2)
rnd_search_cv.fit(X_train, y_train, epochs=100,
                  validation_data=(X_valid, y_valid), 
                  callbacks=[keras.callbacks.EarlyStopping(patience=10)])

#%%
# Optimal model
model = rnd_search_cv.best_estimator_.model()
# n_hidden=2
# n_neurons=30
# learning_rate=0.006611859147852619

# Compute accuracy of model
def get_acc(model, model_name):
    accuracy = round(model.score(X_test, y_test), 4)
    print(f'{model_name} Accuracy: {accuracy}')
    acc_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 'nn_acc.txt'))
    with open(acc_file, 'w') as f:
        f.write(f'{model_name} Accuracy: {accuracy}')
    
get_acc(rnd_search_cv, "Neural Network")

# Export model
model_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                          'nn_model.pkl'))
pickle.dump(model, open(model_file, 'wb'))
