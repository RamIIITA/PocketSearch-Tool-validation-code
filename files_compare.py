#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:01:35 2019

@author: ram
"""

import csv
import platform
import os
pf = '//'
if platform.system() == 'Windows':
    pf= '\\'
    
Dir_3 = ['Neighbour_2', 'Neighbour_3']#, 'Neighbour_4']#, 'Neighbour_5', 'Neighbour_6', 'Neighbour_7']
Dir_4 = ['Buried_2', 'Buried_3', 'Buried_4', 'Buried_5', 'Buried_6', 'Buried_7', 
             'Buried_8', 'Buried_9', 'Buried_10', 'Buried_11', 'Buried_12', 'Buried_13', 'Buried_14']
header = ['pdb', '1.pdb', '2.pdb', '3.pdb', '4.pdb', '5.pdb'] 
    
def get_cavity(f):
    residues = set()
    with open(f, 'r') as pdbfile:
        for line in pdbfile:
            if line.startswith('ATOM'):
                st = line[17:21].strip()+line[23:28].strip()
                residues.add(st.strip())
    return residues



def calculate_accuracy(residue, path, nn, bb, pdb):
    accuracy_list= []
    for each_cavity in ['1.pdb', '2.pdb', '3.pdb', '4.pdb', '5.pdb']:
        try:
            predicted = get_cavity(path+pf+nn+pf+bb+pf+pdb[:4]+pf+each_cavity)
            correct = 0
            for c in residue:
                if c in predicted:
                    correct +=1
            accuracy = correct/len(residue)
            if accuracy == 0.0 or accuracy == 1.0:
                 accuracy_list.append(round(accuracy))
            else:  
                accuracy_list.append(round(accuracy, 2))
        except (FileNotFoundError, IOError):
            accuracy_list.append(-1)
    return accuracy_list


def Create_csv(path, pdbs, op, output_folder, csvf):
    #Dir_1 = ['Output_210']
    #Dir_2 = ['Surface_210']   
    global Dir_3
    global Dir_4
    global header
    csvf = "CSV_Files" 
    if csvf not in os.listdir(path+pf+op):
        os.mkdir(path+pf+op+pf+csvf)
    
    for nn in Dir_3:      
        if nn not in os.listdir(path+pf+op+pf+csvf):
            os.mkdir(path+pf+op+pf+csvf+pf+nn)
        for bb in Dir_4: 
            header = ['pdb', '1.pdb', '2.pdb', '3.pdb', '4.pdb', '5.pdb'] #       
            with open(path+pf+op+pf+csvf+pf+nn+pf+bb+'_csv_file.csv', 'w') as csvfile:
                fieldnames = header
                writer = csv.DictWriter(csvfile, fieldnames = fieldnames)
                writer.writeheader()
                for pdb in pdbs:
                    residue = get_cavity(path+pf+op+pf+output_folder+pf+pdb)
                    accuracy_list = calculate_accuracy(residue, path, nn, bb, pdb)
                    writer.writerow({'pdb':pdb[:-4], '1.pdb': accuracy_list[0], 
                                     '2.pdb': accuracy_list[1],
                                     '3.pdb': accuracy_list[2], 
                                     '4.pdb': accuracy_list[3],
                                     '5.pdb':accuracy_list[4]})               
    print("Succeccful CSV file creations")