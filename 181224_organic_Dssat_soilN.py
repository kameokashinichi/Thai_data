#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 24 17:31:58 2018

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
181224 Compare Dssat result between 5 patterns.
1. one-time organic fertilizer(600kg/ha, 1.5%Ncontent)->SSKT8601
2. one-time organic fertilizer(600kg/ha, 3.5%Ncontent)->﻿SSKT8602_2
3. two-time organic fertilizer(First:300kg/ha-170doy, Second:600kg/ha 210doy, 3.5%Ncontent)-> ﻿SSKT8603
4.two-time organic fertilizer(First:300kg/ha-170doy, Second:600kg/ha 210doy, 3.5%Ncontent) with indicating hard-pan layer->SSKT8604
5. two-time organic fertilizer(First:300kg/ha-170doy, Second:600kg/ha 210doy, 3.5%Ncontent) and inorganic fertilizer(110kg/ha in total) with indicating hard-pan layer->SSKT8605

Second, compare soil N contents
"""


#1 read SSKT8601.OSN
record = []
with open('181206_sskt_sqx1/SSKT8601.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df1 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#1 read SSKT8604.OSN
record = []
with open('181220_SSKT8604_SQX/SSKT8604.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df4 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#1 read SSKT8602.OSN
record = []
with open('181220_SSKT8602SQX_2/SSKT8602_2.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df2 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#1 read SSKT8603.OSN
record = []
with open('181220_SSKT8603_SQX/SSKT8603.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df3 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

#1 read SSKT8605.OSN
record = []
with open('181221_SSKT8605_SQX/SSKT8605.OSN', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

nitro_df5 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

"""
['DOY': day of year,
 'DAS': day after sowing,
 'NAPC': Inorganic N applied (kg/ha),
 'NI#M': N applications (no),
 'NLCC': N leached (kg [N]/ha),
 'NIAD': Total soil NO3+NH4 (kg [N]/ha),
 'NITD': Total soil NO3 (kg [N]/ha),
 'NHTD': Total soil NH4 (kg [N]/ha),
 'NMNC': Cumulative N mineralization (kg [N]/ha),
 'NITC': Cumulative nitrification (kg [N]/ha),
 'NDNC': Cumulative denitrification (kg [N]/ha),
 'NIMC': Cumulative N immobilization (kg [N]/ha),
 'AMLC': Cumulative ammonia volatilization (kg [N]/ha),
 'NNMNC': Cumulative net N mineralization (miner - immob),
 'NUCM': N uptake during season (kg [N]/ha)
 
 'NI1D', 'NI2D', 'NI3D', 'NI4D', 'NI5D', 'NI6D', 'NI7D', 'NI8D',
 'NH1D', 'NH2D', 'NH3D', 'NH4D', 'NH5D', 'NH6D', 'NH7D', 'NH8D',
 ]
"""

#compare the NO3 contents in soil surface layer
fig = plt.figure(figsize = (12,6))
ax = fig.add_subplot(1,1,1)

lis = [nitro_df1, nitro_df2, nitro_df3, nitro_df4, nitro_df5]

for i in range(len(lis)):
    ax.plot(np.arange(0, len(lis[i].index)), lis[i]["NI1D"], 
            color=cm.hsv(i/len(lis)), label="SSKT860"+repr(i+1))

plt.legend(loc="best")
plt.xticks(np.linspace(0, len(lis[i].index), 31), np.arange(1986, 2017, 1))
plt.title("Soil surface NO3 content in each situation", fontsize=18)
plt.xlabel('Year', fontsize=15)
plt.ylabel('Soil surface NO3(ppm)', fontsize=15)
ax.set_xlim(0, 30)
#ax.set_ylim(0, 100)
#plt.savefig('181224_Dssat_png/181224_comparison_of_yield_5pattern.png', bbox_inches='tight')
plt.show()


def genDaysInEachYear(year):
    if year%4 == 0:
        return 366
    else:
        return 365

def genDaysFromParticularYear(year, pyear):
    if year == pyear:
        return 0
    else:
        ynum = 0
        ylist = np.arange(pyear+1, year+1, 1)
        for i in ylist:
            ynum = ynum + genDaysInEachYear(i)
        
        return ynum

#generate the number of the day in each simulation
lis2 = []
for i in range(len(lis)):
    days = []    
    for j in range(len(lis[i].index)):
        day = lis[i].iloc[j, 0] + genDaysFromParticularYear(int(lis[i].index[j]), 1986)
        days.append(day)
        
    lis2.append(np.asarray(days))

#prepare df for "NI1D"(a lot of Nan data)
for i in range(len(lis)):
    if i == 0:
        a = pd.DataFrame(lis[i]["NI1D"].values, index=lis2[i], columns=["SSKT860"+repr(i+1)])
    else:
        b = pd.DataFrame(lis[i]["NI1D"].values, index=lis2[i], columns=["SSKT860"+repr(i+1)])
        a = pd.concat([a,b], axis=1)

#visualize the NO3 contents in each patterns
fig = plt.figure(figsize = (12,6))
ax = fig.add_subplot(1,1,1)

lis = [nitro_df1, nitro_df2, nitro_df3, nitro_df4, nitro_df5]
lis2 = []
for i in range(len(lis)):
    days = []    
    for j in range(len(lis[i].index)):
        day = lis[i].iloc[j, 0] + genDaysFromParticularYear(int(lis[i].index[j]), 1986)
        days.append(day)
        
    lis2.append(np.asarray(days))

for i in range(len(lis)):
    ax.plot(lis2[i], lis[i]["NI1D"], 
            color=cm.hsv(i/len(lis)), label="SSKT860"+repr(i+1))

plt.legend(loc="best")
plt.xticks(np.linspace(0,lis2[3][len(lis2[3])-1],31), np.arange(1986, 2017, 1))
plt.title("Soil surface NO3 content in each situation", fontsize=18)
plt.xlabel('days from 1986', fontsize=15)
plt.ylabel('Soil surface NO3(ppm)', fontsize=15)
ax.set_xlim(4500, 6000)
#ax.set_ylim(0, 100)
plt.savefig('181224_Dssat_png/181225_NO3_surface_5pattern_1998_2001.png', bbox_inches='tight')
plt.show()

#

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    