#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 22:23:46 2023

@author: nicolegordon
"""

from flask import Flask, jsonify, request
import pandas as pd
import os 
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
# declare constants
HOST = '0.0.0.0'
PORT = 8081
# initialize flask application
app = Flask(__name__)
@app.route('/api/train', methods=['POST'])
def train():
    # Read in the cleaned data
    wdir = r'/Users/nicolegordon/Documents/DS/Capstone'
    data = pd.read_csv(os.path.join(wdir, 'cleanData.csv'))
    data = data.drop(columns=['game_id', 'final_score', 'opp_final_score'])
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
    # persist model
    joblib.dump(log_reg, 'model.pkl')
    return jsonify({'accuracy': round(log_reg.score(X_train_transformed, y_train)
                                      * 100, 2)})

@app.route('/api/predict', methods=['POST'])
def predict():
    # get input object from request
    X = request.get_json()

    # read model
    log_reg = joblib.load('model.pkl')
    probabilities = log_reg.predict_proba(X)

    return jsonify([{'name': 'Win', 
                     'value': round(probabilities[0, 0] * 100, 2)}])

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)