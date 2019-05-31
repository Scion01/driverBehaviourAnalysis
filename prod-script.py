#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 30 07:22:20 2019

@author: scion01
"""

import numpy as np
import pandas as pd
import keras
import math
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.models import load_model
from tensorflow.keras.models import model_from_json
from flask import request
from flask import Flask
from flask_cors import CORS, cross_origin
import json
import os
import main_script as ms

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/signal_service', methods=["GET"])
@cross_origin()
def singal_service():
   return "Flask service is up!"
@app.route('/dba_svm_service', methods=["GET"])
def dba_svm_service():
    dataset = pd.read_csv('feature_outputs/2019-05-30 20:08:36.csv')

    X = dataset.iloc[:, 1:7].values
    y = dataset.iloc[:, 10].values
    
    for count in range(0,len(y)):
        if y[count] <9.0:
            y[count]=0
        else:
            y[count]=1
    
    from sklearn.svm import SVC
    classifier = SVC(gamma='auto', kernel = 'rbf', random_state = 0)
    classifier.fit(X,y)
    
    file_name = request.args.get('name')
    file_name = file_name.split('GMT')[0]
    file_name = file_name.replace(':','_')
    
    file_arr = os.listdir()
    
    for i in file_arr:
        if i.find(file_name) != -1:
            file_name = i
            break
    print(file_name)
    ms_obj = ms.main_script(file_name)
    feature_vec_file = ms_obj.generate_feature_vectors()
    print(feature_vec_file)
    dataset_pred = pd.read_csv(feature_vec_file)
    
    X_pred = dataset_pred.iloc[:, 1:7].values
    y_pred = classifier.predict(X_pred)
    
    y_pred_label = [None]*len(y_pred)
    
    for i in range(0,len(y_pred)):
        if(y_pred[i]<0.90):
            y_pred_label[i]="Bad"
        else:
            y_pred_label[i]="Good"
    good = 0 
    bad = 0 
    for i in y_pred_label:
        if i == "Bad":
            bad=bad+1
        else:
            good=good+1
    data = {}
    data['good'] = good
    data['bad'] = bad
    response_data = json.dumps(data)
    return response_data

@app.route('/dba_ann_service',methods = ['GET'])
def dba_ann_service():
    #return request.args.get('name')
    json_file = open('model_dba.json', 'r')
    
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    
    # load weights into new model
    loaded_model.load_weights("model_dba.h5")
    
    loaded_model.save('model_dba.hdf5')
    loaded_model=load_model('model_dba.hdf5')
    
    file_name = request.args.get('name')
    file_name = file_name.split('GMT')[0]
    file_name = file_name.replace(':','_')
    
    file_arr = os.listdir()
    
    for i in file_arr:
        if i.find(file_name) != -1:
            file_name = i
            break
    print(file_name)
    ms_obj = ms.main_script(file_name)
    feature_vec_file = ms_obj.generate_feature_vectors()
    print(feature_vec_file)
    dataset = pd.read_csv(feature_vec_file)
    X = dataset.iloc[:, 1:7].values
    y_pred = loaded_model.predict(X)
    
    y_pred_label = [None]*len(y_pred)
    
    for i in range(0,len(y_pred)):
        if(y_pred[i]<0.90):
            y_pred_label[i]="Bad"
        else:
            y_pred_label[i]="Good"
    good = 0 
    bad = 0 
    for i in y_pred_label:
        if i == "Bad":
            bad=bad+1
        else:
            good=good+1
    data = {}
    data['good'] = good
    data['bad'] = bad
    response_data = json.dumps(data)
    return response_data
if __name__ == '__main__':
   app.run('0.0.0.0',9240)