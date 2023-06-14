#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 22:23:46 2023

@author: nicolegordon
"""

from flask import Flask, jsonify, request
import os 
import joblib
import logging

# logging.basicConfig(filename='record.log', level=logging.DEBUG)
# declare constants
HOST = '0.0.0.0'
PORT = 8081
# initialize flask application
app = Flask(__name__)

@app.route('/api/predict', methods=['POST'])
def predict():
    # get input object from request
    X = request.get_json()

    # read model
    wdir = r'/Users/nicolegordon/Documents/DS/Capstone'
    model_file = os.path.join(wdir, 'model.pkl')
    log_reg = joblib.load(model_file)
    probabilities = log_reg.predict_proba(X)

    return jsonify([{'name': 'Win', 
                      'value': round(probabilities[0, 0] * 100, 2)}])

if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,  # automatic reloading enabled
            port=PORT)