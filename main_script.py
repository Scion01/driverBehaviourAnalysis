#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  5 22:25:18 2019

@author: scion01
"""
import data_preprocessing as pre
import global_vals as global_vals

class main_script:
    def __init__(self):
        preprocess = pre.data_preprocess()
        self.dataset = preprocess.clean()
        
    def get_dataset(self):
        return self.dataset
    
    def generate_feature_vectors(self):
        self.data_rows = self.dataset.iloc[:,:-1].values.tolist()
        self.feature_vector = {}
        #add angle detection logic here
        speed = self.dataset.Speed.values
        acc = self.dataset.accZ.values
        gyro = self.dataset.gyroZ.values
        print(len(self.data_rows))
        for row_count in range(len(self.data_rows)):
            feature_element = {}
            max_speed = 0
            min_speed = 999
            avg_speed = 0
            max_acc = 0
            min_acc =999
            avg_acc = 0
            max_rotation = 0
            min_rotation = 999
            avg_rotation = 0
            count=0
            if (row_count+global_vals.sample_size>len(self.data_rows)):
                global_vals.sample_size = global_vals.sample_size - row_count - 1
            while count in range(global_vals.sample_size):
                max_speed = abs(speed[row_count+count]) if abs(speed[row_count+count])>max_speed else max_speed
                max_rotation = abs(gyro[row_count+count]) if abs(gyro[row_count+count])>max_rotation else max_rotation
                max_acc = abs(acc[row_count+count]) if abs(acc[row_count+count])>max_acc else max_acc

                avg_speed+=speed[row_count+count]
                avg_acc+=acc[row_count+count]
                avg_rotation+=gyro[row_count+count]
                
                min_speed = abs(speed[row_count+count]) if abs(speed[row_count+count])<min_speed else min_speed
                min_rotation = abs(gyro[row_count+count]) if abs(gyro[row_count+count])<min_rotation else min_rotation
                min_acc = abs(acc[row_count+count]) if abs(acc[row_count+count])<min_acc else min_acc
                count+=1
            
            if(count>0):
                avg_acc/=global_vals.sample_size
                avg_speed/=global_vals.sample_size
                avg_rotation/=global_vals.sample_size
                
                feature_element['max_speed'] = max_speed
                feature_element['max_rotation'] = max_rotation
                feature_element['max_acc'] = max_acc
                feature_element['avg_acc'] = avg_acc
                feature_element['avg_rotation'] = avg_rotation
                feature_element['avg_speed'] = avg_speed
                feature_element['min_acc'] = min_acc
                feature_element['min_speed'] = min_speed
                feature_element['min_rotation'] = min_rotation
                
                self.feature_vector[row_count] = feature_element

        return self.feature_vector


main_script_obj = main_script()
print(main_script_obj.generate_feature_vectors())
