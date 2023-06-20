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

# declare constants
HOST = '0.0.0.0'
PORT = 4500
# initialize flask application
app = Flask(__name__)
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/api/predict', methods=['POST'])
def predict():
    # get input object from request
    X = request.get_json()

    # read model
    wdir = r'/Users/nicolegordon/Documents/DS/Capstone'
    model_file = os.path.join(wdir, 'model.pkl')
    log_reg = joblib.load(model_file)
    probabilities = log_reg.predict_proba(X)
    # probabilities = [0]

    return jsonify([{'name': 'Win', 
                      'value': round(probabilities[0] * 100, 2)}])


if __name__ == '__main__':
    # run web server
    app.run(host=HOST,
            debug=True,
            port=PORT)
