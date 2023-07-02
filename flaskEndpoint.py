#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 22:23:46 2023

@author: nicolegordon
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import os 
import joblib
import pandas as pd

# declare constants
HOST = '0.0.0.0'
PORT = 4500
# initialize flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/predict', methods=['POST'])
def predict():
    # get input object from request
    request_data = pd.DataFrame(request.get_json(), index=[0])
    # calculate score differential
    score_differential = int(request_data.homeScore) - int(request_data.awayScore)
    # check if home has possession
    is_home_possesion = (request_data.possessionTeam == request_data.homeTeam)
    # put data into data frame to match model
    X = pd.DataFrame({'qtr': int(request_data.quarter),
                      'cur_home_score': int(request_data.homeScore),
                      'cur_away_score': int(request_data.awayScore),
                      'score_differential': score_differential,
                      'week': int(request_data.week),
                      'home_possession': int(is_home_possesion),
                     },
                     index=[0])

    # read in model
    model_file = os.path.abspath(os.path.join(os.path.dirname( __file__ ), 
                                              'models', 'rf_model.pkl'))
    model = joblib.load(model_file)
    
    # predict win probability
    probabilities = model.predict_proba(X)[0]
    
    # return win probability to frontend
    return jsonify({'name': request_data.homeTeam.values[0], 
                      'value': round(probabilities[1] * 100, 2)})


if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,
            port=PORT)
