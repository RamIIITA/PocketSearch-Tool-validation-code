#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 13:22:25 2019

@author: ram
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import csv
import platform
import os
from files_compare import Dir_3, Dir_4


pf = '/'
if platform.system() == 'Windows':
    pf= '\\'

def Correctly_predicited_each_pdb(file, Threshold):
    with open(file, 'r') as csvfile:
        predicted = 0
        csv_reader = csv.reader(csvfile, delimiter=',')
        for row in csv_reader:
            if (row[0]).lower() != 'pdb':
                row_max = max(list(map(float, row[1:])))
                if row_max >= Threshold:
                    predicted+=1
    return predicted


def Correctly_predicited_all_buriedness(path,f, nn,Threshold):
    Burried_array = []
    for each_csv in Dir_4:
        csv = Correctly_predicited_each_pdb(path+pf+nn+pf+each_csv+"_csv_file.csv", Threshold)
        Burried_array.append(csv)
    Burried_array.append(max(Burried_array))
    return Burried_array


def Create_csv(path,f,Threshold):    
    Dir_4 = ['Neighbourhood','Buried_2', 'Buried_3', 'Buried_4', 'Buried_5', 'Buried_6', 'Buried_7', 
             'Buried_8', 'Buried_9', 'Buried_10', 'Buried_11', 'Buried_12', 'Buried_13', 'Buried_14','Maximum']
   
    csvfile = open(path+pf+f, 'w')
    header =  Dir_4
    writer = csv.DictWriter(csvfile, fieldnames = header)
    writer.writeheader()

    for nn in Dir_3:
        dic= {}            
        with open(path+pf+f, 'a') as csvfile:            
            writer = csv.DictWriter(csvfile, fieldnames = header)            
            accuracy_list = [nn]+Correctly_predicited_all_buriedness(path,f,nn,Threshold)            
            #print(accuracy_list)
            for key,value in zip(Dir_4, accuracy_list):
                dic[key] = value
            writer.writerow(dic)
            
    csvfile.close()    
    print("Matrix file is created")



















