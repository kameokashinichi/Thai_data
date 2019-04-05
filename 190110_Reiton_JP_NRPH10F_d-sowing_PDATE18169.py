#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 10 14:41:49 2019

@author: kameokashinichi
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil
from pylab import cm
from statistics import mean, stdev, median
from sklearn import linear_model
from mpl_toolkits.mplot3d import Axes3D

"""
190108_Dssat spil-water relation file
http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/cropsim/exec/2019-01-10T05-38-16-196Z0dd6e68de7570f4c
soilid -> "JP_NRPH10F"
planting method -> transplanting
planting date -> 18143

soilWat.OUT, Summary.OUT, SoilNi.OUT, PlantN.OUT, 100 weather scenarios
"""
"""
190110 read water stress Dssat file.(SoilWat.OUT)
"""

soilW = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/SoilWat.OUT', 'r') as f:
    for row in f:
        soilW.append(row.strip())
        
soilW = soilW[12:]        

#separate each rows by empty letter        
stress = []     
for row in soilW:
    element = row.split()
    stress.append(element)   
        
columns = stress[0]

#extract available rows
stress = np.asarray(stress)
num = []
for i in range(len(stress)):
    if stress[i] == columns:
        pass
    elif len(stress[i]) != 22:
        pass
    else:
        num.append(i)

sw = stress[num]

"""
for i in range(len(sw)):
    if len(sw[i]) != 21:
        print(i)
"""

#convert list to np.array    
s_stress = []
for i in range(len(sw)):
    s_stress.append(sw[i])
s_stress = np.asarray(s_stress)    

sw_df = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = s_stress[:,0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(sw_df.index)):
    if i == len(sw_df.index)-1:
        break
    elif int(sw_df.iloc[i, 0]) > int(sw_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(sw_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
sw_df5T = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)
 
"""
190108 Summary.OUT
"""
record = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

"""
190108 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/SoilNi.OUT', 'r') as f:
    for row in f:
        soilN.append(row.strip())
        
soilN = soilN[12:]        

#separate each rows by empty letter        
stressN = []     
for row in soilN:
    element = row.split()
    stressN.append(element)   
        
columns = stressN[0]

#extract available rows
stressN = np.asarray(stressN)
num = []
for i in range(len(stressN)):
    if stressN[i] == columns:
        pass
    elif len(stressN[i]) != 30:
        pass
    else:
        num.append(i)
sn = stressN[num]

"""
for i in range(len(sn)):
    if len(sn[i]) != 28:
        print(i)
"""

#convert list to np.array
sn_stress = []
for i in range(len(sn)):
    sn_stress.append(sn[i])
sn_stress = np.asarray(sn_stress)

sn_df = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = sn_stress[:, 0])    

#change the index from year to simulation number
number = [0]
for i in range(len(sn_df.index)):
    if i == len(sn_df.index)-1:
        break
    elif int(sn_df.iloc[i, 0]) > int(sn_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(sn_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
sn_df5T = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = newcol) 

"""
190108 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/PlantN.OUT', 'r') as f:
    for row in f:
        PN.append(row.strip())
        
PN = PN[10:]

#separate each rows by empty letter        
stressPN = []     
for row in PN:
    element = row.split()
    stressPN.append(element)   
        
columns = stressPN[0]

#extract available rows
stressPN = np.asarray(stressPN)
num = []
for i in range(len(stressPN)):
    if stressPN[i] == columns:
        pass
    elif len(stressPN[i]) != 18:
        pass
    else:
        num.append(i)
        
pn = stressPN[num]
"""
for i in range(len(pn)):
    if len(pn[i]) != 18:
        print(i)
"""

#convert list to np.array
pn_stress = []
for i in range(len(pn)):
    pn_stress.append(pn[i])
pn_stress = np.asarray(pn_stress)

#convert np.ndarray to pd.DataFrame
pn_df = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = pn_stress[:, 0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(pn_df.index)):
    if i == len(pn_df.index)-1:
        break
    elif int(pn_df.iloc[i, 0]) > int(pn_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(pn_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
pn_df5T = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = newcol)


"""
190108 PlantGro.OUT degree days etc.
"""

PG = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/PlantGro.OUT', 'r') as f:
    for row in f:
        PG.append(row.strip())
        
PG = PG[13:]

stress = []     
for row in PG:
    element = row.split()
    stress.append(element)   
        
columns = stress[0]

#extract available rows
stress = np.asarray(stress)
num = []
for i in range(len(stress)):
    if len(stress[i]) == 36 and stress[i][0] == '2018':
        num.append(i)
    else:
        pass

pg = stress[num]

"""
for i in range(len(sw)):
    if len(sw[i]) != 21:
        print(i)
"""

#convert list to np.array    
pg_stress = []
for i in range(len(pg)):
    pg_stress.append(pg[i])
pg_stress = np.asarray(pg_stress)    

pg_df = pd.DataFrame(pg_stress[:, 1:], columns=columns[1:], index = pg_stress[:,0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(pg_df.index)):
    if i == len(pg_df.index)-1:
        break
    elif int(pg_df.iloc[i, 0]) > int(pg_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(pg_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
pg_df5T = pd.DataFrame(pg_stress[:, 1:].astype(np.float32), columns=columns[1:], index = newcol)