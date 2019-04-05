#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 22 07:20:27 2018

@author: kameokashinichi
"""

import os
import pickle
import numpy as np
import pandas as pd
import re
import shutil
from statistics import mean, stdev, median
import matplotlib.pyplot as plt
from pylab import cm
from weatherAPI import extractWTHFromDirectory
from sklearn import linear_model


"""
181222 confirm SSKT8602 results
1. OSN
2. OPN
3. OSU
"""

#1 read SSKT8605.OSN
record = []
with open('181220_SSKT8602SQX_2/SSKT8602_2.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df4 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#2 read SSKT8605.OPN to check the Nitrogen absorbance by plant
record = []
with open('181220_SSKT8602SQX_2/SSKT8602_2.OPN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitroP = []
for i in range(len(record)):
    if re.search('^\d{4}', record[i]):
        nitroP.append(record[i].split())

nitroP = np.asarray(nitroP)
nitroP = np.delete(nitroP, 9, axis=1)
nitro2 = np.asarray(nitroP[1:, 1:], dtype=np.float64)

col = np.array(record[10].split())
col = np.delete(col, 9)
nitroP_df4 = pd.DataFrame(nitro2, index=nitroP[1:, 0], columns=col[1:])

#3. read SSKT8605.OSU
record = []
with open('181220_SSKT8602SQX_2/SSKT8602_2.OSU', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(3, len(record)):
    nitro.append(record[i].split())
    
#nitro[0] = nitro[0][1:]
nitro = np.asarray(nitro)
nitro = nitro[:, 10:]
nitro = np.delete(nitro, 1, axis=1)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

sum_df4 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

num = np.arange(0, 60, 2)
sum_df4 = sum_df4.iloc[num]  #delete fallow index


#visualize the N flow between soil and plant.
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

dfs = searchElementforX(nitro_df4, '1988')
dfp = searchElementforX(nitroP_df4, '1988')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NI1D'], color='brown', label='soil NO3')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NH1D'], color='orange', label='soil NH4')
ax.legend(bbox_to_anchor=(0.3, 1.0), fontsize=13)

ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'VNAD'], color='green', label='plant')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'CNAD'], color='red', label='top')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')

ax2.legend(bbox_to_anchor=(1.0, 0.7), fontsize=13)
#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(ppm)", fontsize=15)
ax2.set_ylabel('nitrogen contents in plant(kg/ha)', fontsize=15)
plt.title("N stream between soil and plant", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(200, 350)
#ax.set_ylim(0, 30)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()



"""
181222 confirm SSKT8604 results
1. OSN
2. OPN
3. OSU
"""

#1 read SSKT8605.OSN
record = []
with open('181220_SSKT8604_SQX/SSKT8604.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df2 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#2 read SSKT8605.OPN to check the Nitrogen absorbance by plant
record = []
with open('181220_SSKT8604_SQX/SSKT8604.OPN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitroP = []
for i in range(len(record)):
    if re.search('^\d{4}', record[i]):
        nitroP.append(record[i].split())

nitroP = np.asarray(nitroP)
nitroP = np.delete(nitroP, 9, axis=1)
nitro2 = np.asarray(nitroP[1:, 1:], dtype=np.float64)

col = np.array(record[10].split())
col = np.delete(col, 9)
nitroP_df2 = pd.DataFrame(nitro2, index=nitroP[1:, 0], columns=col[1:])

#3. read SSKT8605.OSU
record = []
with open('181220_SSKT8604_SQX/SSKT8604.OSU', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(3, len(record)):
    nitro.append(record[i].split())
    
#nitro[0] = nitro[0][1:]
nitro = np.asarray(nitro)
nitro = nitro[:, 10:]
nitro = np.delete(nitro, 1, axis=1)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

sum_df2 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

num = np.arange(0, 62, 2)
sum_df2 = sum_df2.iloc[num]  #delete fallow index

#visualize the N flow between soil and plant.
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

dfs = searchElementforX(nitro_df2, '1988')
dfp = searchElementforX(nitroP_df2, '1988')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NI1D'], color='brown', label='soil NO3')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NH1D'], color='orange', label='soil NH4')
ax.legend(bbox_to_anchor=(0.3, 1.0), fontsize=13)

ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'VNAD'], color='green', label='plant')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'CNAD'], color='red', label='top')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')

ax2.legend(bbox_to_anchor=(1.0, 0.7), fontsize=13)
#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(ppm)", fontsize=15)
ax2.set_ylabel('nitrogen contents in plant(kg/ha)', fontsize=15)
plt.title("N stream between soil and plant", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(200, 350)
#ax.set_ylim(0, 30)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()

#pick up several weather data
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in 1987, 1988, 1989, 1990, 2000:
    num = repr(i)[2:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
    color=cm.Reds(sum_df4.loc["SSKT"+num+"01", "HWAH"]/max(hwah4)), 
    label=repr(i)+'(y='+repr(sum_df4.loc["SSKT"+num+"01", "HWAH"])+')')
    #print(i)
    
plt.legend(loc='best')
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Rain Fall (TPDOY=215)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Rain Fall (mm)', fontsize=15)
ax.set_xlim(200, 300)
ax.set_ylim(0, 100)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()

















