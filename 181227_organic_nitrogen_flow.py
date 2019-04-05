#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 27 06:36:52 2018

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
from matplotlib.patches import Polygon

"""
181227 analyze the total N uptake(NUCM) in each simulation

nitro_df1, nitro_df4, nitro_df5
"""

#generate the list which contains total N uptake in each year
sskt = WTD2DataFrame("SSKT.WTD")

lis1 = []
for i in range(1986, 2016):
    df = searchElementforX(nitro_df1, repr(i))
    nucm = sum(df["NUCM"])
    lis1.append(nucm)

lis4 = []
for i in range(1986, 2017):
    df = searchElementforX(nitro_df4, repr(i))
    nucm = sum(df["NUCM"])
    lis4.append(nucm)
    
lis5 = []
for i in range(1986, 2017):
    df = searchElementforX(nitro_df5, repr(i))
    nucm = sum(df["NUCM"])
    lis5.append(nucm)


#visualize the result

fig = plt.figure(figsize = (12, 6))
ax = fig.add_subplot(1,1,1)

lis = [lis1, lis4, lis5]

for i in range(len(lis)):
    ax.plot(np.arange(len(lis[i])), lis[i], color=cm.hsv(i/len(lis)),
            label="pattern"+repr(i+1))

plt.legend(loc='best', fontsize=15)
plt.title("amount of N uptake in each simulation", fontsize=18)
plt.xticks(np.arange(0, len(lis[i]), 5), np.arange(1986, 1986+len(lis[i]), 5))
plt.xlabel('Year', fontsize=16)
plt.ylabel("N uptake (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181224_Dssat_png/181227_Amount_of_N_uptake.png')

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

#compare the amount of N in soil        
#generate the number of the day in each simulation
lis = [nitro_df1, nitro_df4, nitro_df5]
        

nday = []
for i in range(len(lis)):
    days = []    
    for j in range(len(lis[i].index)):
        day = lis[i].iloc[j, 0] + genDaysFromParticularYear(int(lis[i].index[j]), 1986)
        days.append(day)
        
    nday.append(np.asarray(days))

"""
#prepare df for "NIAD"(a lot of Nan data)
for i in range(len(lis)):
    if i == 0:
        a = pd.DataFrame(lis[i]["NIAD"].values, index=lis2[i], columns=["SSKT860"+repr(i+1)])
    else:
        b = pd.DataFrame(lis[i]["NIAD"].values, index=lis2[i], columns=["SSKT860"+repr(i+1)])
        a = pd.concat([a,b], axis=1)
"""

#visualize the total nitrogen contents in each patterns
fig = plt.figure(figsize = (14,6))
ax = fig.add_subplot(1,1,1)

lis = [nitro_df1, nitro_df4, nitro_df5]

for i in range(len(lis)):
    ax.plot(nday[i], lis[i]["NIAD"], 
            color=cm.hsv(i/len(lis)), label="pattern"+repr(i+1))

plt.legend(loc="best")
plt.xticks(np.linspace(0,nday[2][len(nday[2])-1],31), np.arange(1986, 2017, 1))
plt.title("Soil Nitrogen content in each situation", fontsize=18)
plt.xlabel('Year', fontsize=15)
plt.ylabel('Soil Nitrogen content(kg/ha)', fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=15, rotation=45, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#ax.set_xlim(3000, 6000)
#ax.set_ylim(0, 100)
plt.savefig('181224_Dssat_png/181227_Soil_Nitrogen_3pattern.png', bbox_inches='tight')
plt.show()


#visualize the surface NO3 contents in each patterns
fig = plt.figure(figsize = (14,6))
ax = fig.add_subplot(1,1,1)

lis = [nitro_df1, nitro_df4, nitro_df5]

for i in range(len(lis)):
    ax.plot(nday[i], lis[i]["NI1D"], 
            color=cm.hsv(i/len(lis)), label="pattern"+repr(i+1))

plt.legend(loc="best")
plt.xticks(np.linspace(0,nday[2][len(nday[2])-1],31), np.arange(1986, 2017, 1))
plt.title("Soil surface NO3 content in each situation", fontsize=18)
plt.xlabel('Year', fontsize=15)
plt.ylabel('Soil surface NO3 content(ppm)', fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=15, rotation=45, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#ax.set_xlim(3000, 6000)
#ax.set_ylim(0, 100)
plt.savefig('181224_Dssat_png/181227_Soil_Surface_NO3_3pattern.png', bbox_inches='tight')
plt.show()




















        
        


