import platform
from prody import *  #"""used for find the bonds and interactios """     
import os   #"""To work with files and their paths"""
from cofactor_list import dict_cofactor #"""cofactor_list is py file created by our Oown contains cofactor which 
import files_compare as fc
#include salts, metals, organo-metalic complexes, prosthetic groups from various sources"""
import Matrix_file_creation as mfc
import Plot as plot

pf = '/'
if platform.system() == 'Windows':
    pf= '\\'


global_cache = {}

def cached_listdir(path):  # To get the list of files in a directory
    res = global_cache.get(path)
    if res is None:
        res = os.listdir(path)
        global_cache[path] = res
    
    pdbs = []
    for i in res:
        if i[-3:]=='pdb':
            pdbs.append(i)
    return pdbs
            

def ligand_extraction(path, all_pdbs, output_folder, file_name, op):
    list_ligands = {}
    for file in all_pdbs:        
        f = open(path+pf+file_name+pf+file, 'r')
        list_ligands[file] = []
        for line in f:
            if line.startswith('HETATM'):
                cur = line[17:20].strip()
                if cur not in list_ligands[file] and dict_cofactor.get(cur, False)==False:
                    list_ligands[file].append(cur)
    print("Successful creation of pdb and ligand dictory ")                
    return Atom_interactions( path, all_pdbs, list_ligands,output_folder, file_name, op)


def for_multi_ligand_pdbs(path, multi_ligand_pdbs, pdb_ligands, output_folder, file_name, op):
    count = 0
    multiple = []
    for each_pdb in multi_ligand_pdbs:
        for ligand in pdb_ligands[each_pdb]:        
            pdb = parsePDB(path+pf+file_name+pf+each_pdb)
            contacts = pdb.select('protein and within 4 of resname '+ligand)
            pdb = each_pdb[:-4]+'_'+ligand.upper()
            name=path+pf+op+pf+output_folder+pf+pdb
            multiple.append(pdb+'.pdb')
            writePDB(name, contacts)
            #print(each_pdb, ligand, pdb_ligands[each_pdb])
            count += 1
    return count, multiple   

def for_single_ligand_pdbs(path, single_ligand_pdbs, pdb_ligands, output_folder, file_name, op):
    count = 0
    single = []
    for each_pdb in single_ligand_pdbs:             
        pdb = parsePDB(path+pf+file_name+pf+each_pdb)
        contacts = pdb.select('protein and within 4 of resname '+pdb_ligands[each_pdb][0])
        name=path+pf+op+pf+output_folder+pf+each_pdb[:-4]
        single.append(each_pdb)
        writePDB(name, contacts)
        #print(each_pdb, pdb_ligands[each_pdb][0])
        count += 1
    return count, single

def Atom_interactions(path, all_pdbs, pdb_ligands, output_folder, file_name, op):    
    Total_files = 0
    multi_ligand_pdbs = []
    single_ligand_pdbs = []
    
    for each in all_pdbs:
        if len(pdb_ligands[each]) > 1:
            multi_ligand_pdbs.append(each)
        elif len(pdb_ligands[each])== 1:
            single_ligand_pdbs.append(each)
    
    print("\nTotal Single ligand files: ", len(single_ligand_pdbs))
    print("\nTotal Multiple ligand files: ", len(multi_ligand_pdbs))
    
    multi_ligand_pdbs.sort()
    single_ligand_pdbs.sort()
    
    single, s = for_single_ligand_pdbs(path, single_ligand_pdbs, pdb_ligands, output_folder, file_name, op)
    multi, m = for_multi_ligand_pdbs(path, multi_ligand_pdbs, pdb_ligands, output_folder, file_name, op)
    
    Total_files = single+multi       
    print("\n\nTotal no. Files are created ",Total_files)
    return s+m
    


""" INPUT part """
#/home/ram/Desktop/Thesis/Rahul_sir/PDB_210


path = input("Enter the PDB's File path:")
file_name = 'PDB_210'#input("Enther the PDB's file name:")
all_pdbs = cached_listdir(path+pf+file_name)
op = "Module Output files"
output_folder = "Atomicinteractions of Source PDBs"


if op not in os.listdir(path):
    os.mkdir(path+pf+op)


if output_folder not in os.listdir(path+pf+op):
    os.mkdir(path+pf+op+pf+output_folder)

all_pdbs = ligand_extraction(path, all_pdbs, output_folder, file_name, op)

csvf = "CSV_Files"
fc.Create_csv(path, all_pdbs, op, output_folder, csvf)

f = "Matrix_of_all_files.csv"
Threshold = 0.8 #float(input("Please Enter the threshold accuracy to predict"))
mfc.Create_csv(path+pf+op+pf+csvf, f, Threshold)

plots = "Plots"
if plots not in os.listdir(path+pf+op):
    os.mkdir(path+pf+op+pf+plots)
    
plot.plot_matrix_file(path,op,csvf, plots,f)

