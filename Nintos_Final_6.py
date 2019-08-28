import csv
import pandas as pd
import glob
import os
import time
import configparser
from os import path
import shutil


data_rows = []
date_rows = []
output = []
output2= []
output_firstrow = []
time_stamp = time.strftime("%Y%m%d%H%M%S")

def Consolidated_Output(filename,output_path):

    #actFile = filename+'.csv'
    actFile = filename
    clean_file = filename+'_'+time_stamp+'_clean.csv'
    i=0
    with open(actFile, 'r', newline='') as fI, open(clean_file,'w',newline='') as fC:
        reader = csv.reader(fI)
        writer= csv.writer(fC)
        for counter, row in enumerate(reader):
            output.append(row[:])
        print (len(output))
        while i<len(output)-1:
            writer.writerows(r+[""] for r in [output[i]])
            i+=1   
        #print(output)
   
#Seperating the Data columns and the Date Columns
    
    with open(clean_file, 'r', newline='') as fI:
        reader = csv.reader(fI)
        for counter, row in enumerate(reader):
            data_rows.append(row[:17])
            date_rows.append(row[17:])
    #print(data_rows)
    output2= data_rows[0]
    output2.extend(['','Report_Date','Date_Value'])

# Creating the Headers row as a seperate file

    with open(output_path+'\combinedfile-%s_0.csv'%time_stamp,"w",newline="") as f0:
        cw = csv.writer(f0)
        cw.writerows(r+[""] for r in [output2])

# Creating the data row as an individual file    
    i = 1
    while i<= len(data_rows)-1:
        with open(filename+'_datacolumns-'+time_stamp+'_%i.csv'%i,'w',newline='') as fi:
            cw1 = csv.writer(fi)
            cw1.writerows(r+[""] for r in [data_rows[i]])
            i = i+1

# Creating the Dates and Values relevant to the individual row as seperate file        
    j = 1       
    while j <= len(date_rows)-1: 
        with open(filename+'_datecolumns-'+time_stamp+'_%i.csv'%j,'w', newline='') as fI:
            writer = csv.writer(fI)
            rows = zip(date_rows[0],date_rows[j])
            for word in rows:
              writer.writerow(word)
            j+=1



# Creating Dates number of rows for each individual row in a seperate file        
    k = 1
    m = 0
    while k<= len(data_rows)-1:
        with open (filename+'_datacolumns-'+time_stamp+'_%i.csv'%k,'r',newline='') as fo,open(filename+'_datenoof_datacolumns-'+time_stamp+'_%i.csv'%k,'w',newline='') as fi:
            reader = csv.reader(fo)
            writer = csv.writer(fi)
            for counter, row in enumerate(reader):
                output_firstrow.append(row[:17])                
                m=0
                while m <= len(date_rows[0]):
                    writer.writerows(r+[""] for r in [output_firstrow[0]])
                    m+=1    
            output_firstrow.clear()
        k+=1
    
    output_Data = []
    output_Dates = []

# Merging the Data Rows with Date and value columns

    n=1
    while n <= len(data_rows)-1:
        with open(filename+'_datenoof_datacolumns-'+time_stamp+'_%i.csv'%n,'r') as fi1, open(filename+'_datecolumns-'+time_stamp+'_%i.csv'%n,'r') as fi2:
            cw1 = csv.reader(fi1)
            cw2 = csv.reader(fi2)
            for counter, row in enumerate(cw1):
                output_Data.append(row[0:])
            for counter,row in enumerate(cw2):
                output_Dates.append(row[0:])
        with open (output_path+'\combinedfile-'+time_stamp+'_%i.csv'%n,'w', newline='') as ft1:
            cw=csv.writer(ft1)
            for ele_a, ele_b in zip(output_Data,output_Dates):
                ele_a.extend(ele_b)
                cw.writerows(r+[""] for r in [ele_a])
            ele_a.clear()
            output_Data.clear()
            output_Dates.clear()
        n+=1


# Combining the seperate files as a single CSV file.
   
    csv_files = glob.glob(output_path+'\combinedfile-'+time_stamp+'*.csv')
    with open(output_path+'/NINTENDO-'+time_stamp+'.csv','w') as fout:
        for filename in csv_files:
            with open(filename) as fin:
                for line in fin:
                    fout.write(line)
                       

# Removing the blank column

    data = []
    filtered_data = []
    data = pd.read_csv(output_path+'/NINTENDO-'+time_stamp+'.csv',encoding = "ISO-8859-1")
    filtered_data = data.dropna(axis='columns', how = 'all')
    filtered_data.to_csv(output_path+'/NINTENDO-'+time_stamp+'.csv',index=None)
    
    return
#-----------Calling the Main Script------------------------------------
config = configparser.ConfigParser()
config.read('NINT_CONFIG.ini')


inputDet= config['InputDetails']
outputDet= config['OutputDetails']
archiveDet= config['ArchiveDetails']

 
inputPath=inputDet['inputpath']
outputPath=outputDet['outputpath']
archivePath= archiveDet['archivepath']

files = [i for i in os.listdir(inputPath) if i.startswith("NINTENDO_") and path.isfile(path.join(inputPath, i))]

file = files[0]

Consolidated_Output(file,outputPath)

# Archiving the input file

for f in files:
    shutil.move(path.join(inputPath, f), archivePath)

