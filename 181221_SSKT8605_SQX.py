#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 21 14:32:06 2018

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
181221 Confirm Dssat initial profile (SSKT8605.SQX)

OSN OSU OSW OPN
"""
#read SSKT8605.OSN to determine the initial soil NO3 and NH4 content
hwah4 = [2575, 2297, 2497, 2309, 2688, 2051, 2285, 1021, 2443, 2229, 
         2092, 2353, 2309, 2168, 2213, 2279, 2025, 2231, 1093, 2144, 
         2198, 2115, 2267, 2283, 2193, 2506, 2055, 2230, 2118, 1995, 2108]


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

#read SSKT8605.OPN to check the Nitrogen absorbance by plant
record = []
with open('181221_SSKT8605_SQX/SSKT8605.OPN', "r") as f:
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
nitroP_df5 = pd.DataFrame(nitro2, index=nitroP[1:, 0], columns=col[1:])

#read SSKT8605.OSU
record = []
with open('181221_SSKT8605_SQX/SSKT8605.OSU', "r") as f:
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

sum_df5 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

num = np.arange(0, 62, 2)
sum_df5 = sum_df5.iloc[num]  #delete fallow index


#read SSKT8601.OSW
record = []
with open('181221_SSKT8605_SQX/SSKT8605.OSW', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(12, len(record)):
    nitro.append(record[i].split())

nitro = np.asarray(nitro)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

s_wat_df5 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])



#vixualize the soil N movement
fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

dfs = searchElementforX(nitro_df5, '2011')
dfp = searchElementforX(nitroP_df5, '2011')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NI1D'], color='brown', label='soil NO3')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NH1D'], color='orange', label='soil NH4')
ax.legend(bbox_to_anchor=(0.15, 1.0), fontsize=13)

ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'VNAD'], color='green', label='plant')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'CNAD'], color='red', label='top')
ax2.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')

ax2.legend(bbox_to_anchor=(1.0, 0.7), fontsize=13)
#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(ppm)", fontsize=15)
ax2.set_ylabel('nitrogen contents in plant(kg/ha)', fontsize=15)
plt.title("N stream between soil and plant in 2011~high yield~", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(200, 350)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
plt.savefig('181224_Dssat_png/181225_N_flow_in_2011_SSKT8605.png', bbox_inches='tight')
plt.show()


#check the correlation between PRCP(precipitation during planting) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = sum_df5.loc[:, 'PRCP'].values
hwah4 = sum_df5.loc[:, 'HWAH'].values

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Precipitation VS Yield", fontsize=18)
plt.xlabel('Precipitation (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181221_NO3contents_VS_yield.png')

plt.show()

#weather data
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 31):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
    color=cm.Reds(hwah4[i]/max(hwah4)), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    #print(i)
    
plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Rain Fall (TPDOY=215)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Rain Fall (mm)', fontsize=15)
ax.set_xlim(220, 260)
ax.set_ylim(0, 150)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()

#pick up particular year's weather data(RAIN)
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

hwah = sum_df5["HWAH"].values
n = 0
for i in 1990, 2015:
    num = repr(i)[2:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
    color=cm.Reds(sum_df5.loc["SSKT"+num+"01", "HWAH"]/max(hwah)), 
    label=repr(i)+'(y='+repr(sum_df5.loc["SSKT"+num+"01", "HWAH"])+')')
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

#rain fall in the juvenile, vegetative growth season
rain = []
for i in range(0, 31):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    tor = sum(df.loc[num+"270":num+"285", "RAIN"])
    rain.append(tor)

#check the correlation between PRCP(precipitation during juvenile) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(rain)
hwah4 = sum_df5.loc[:, 'HWAH'].values

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Precipitation of DAS 50-60 VS Yield", fontsize=18)
plt.xlabel('Precipitation(50-60 days after seeding) (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()


#compare the with-hardpan and without-hardpan
fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

prep = searchElementforX(sskt, "^01")["RAIN"].values
#srad = searchElementforX(sskt, "^98")["SRAD"].values
ax.plot(np.arange(1, len(prep)+1), prep, color="blue", label="rain fall")
ax.legend(bbox_to_anchor=(0.3, 1.0), fontsize=13)

dfs4 = searchElementforX(nitro_df4, '2001')
dfs3 = searchElementforX(nitro_df3, '2001')
ax2.plot(dfs4.loc[:, 'DOY'], dfs4.loc[:, 'NI1D'], color='red', label='NO3-hardpan')
ax2.plot(dfs4.loc[:, 'DOY'], dfs4.loc[:, 'NH1D'], color='green', label='NH4-hardpan')
ax2.plot(dfs3.loc[:, 'DOY'], dfs3.loc[:, 'NI1D'], color='orange', label='NO3')
ax2.plot(dfs3.loc[:, 'DOY'], dfs3.loc[:, 'NH1D'], color='brown', label='NH4')
ax2.legend(bbox_to_anchor=(0.5, 1.0), fontsize=13)

ax2.set_ylabel("N contents in soil(m2/m2)", fontsize=15)
ax.set_ylabel('Daily rain fall(mm)', fontsize=15)
plt.title("Comparison of the N content in soil between with and without hardpan 2001", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(100, 300)
#ax.set_ylim(0, 30)
plt.savefig('181224_Dssat_png/181225_soil_N_2001_SSKT8603_VS_SSKT8604.png', bbox_inches='tight')
plt.show()


#relation between yield and NO3
juv_no3 = nitro_df5.query("250<DOY<270")
uni = []
for i in range(len(juv_no3.index)):
    if i == 0:
        uni.append(i)
    elif juv_no3.index[i] != juv_no3.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no3_uni = juv_no3.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no3_uni["NH3D"].values
hwah4 = sum_df5.loc[:, 'HWAH'].values[:30]   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3[:30].reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3[:30], hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DOY250) VS Yield-SSKT8605-", fontsize=18)
plt.xlabel('NO3 content in 30cm (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/181230_NO3_15cm_in_DAS35_VS_yield_SSKT8605.png')

plt.show()


#relation between yield and NO3(280<DOY<300)
juv_no3 = nitro_df5.query("290<DOY<310")
uni = []
for i in range(len(juv_no3.index)):
    if i == 0:
        uni.append(i)
    elif juv_no3.index[i] != juv_no3.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no3_uni = juv_no3.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no3_uni["NI1D"].values
hwah4 = sum_df5.loc[:, 'HWAH'].values[:30]   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3[:30].reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3[:30], hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at the end of vegetative growth(DAS70) VS Yield-SSKT8605-", fontsize=16)
plt.xlabel('NO3 content in surface (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181224_Dssat_png/181230_surface_NO3_in_DAS75_VS_yield_SSKT8605.png')

plt.show()


#rain fall in the juvenile, vegetative growth season
rain = []
for i in range(0, 31):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    tor = sum(df.loc[num+"290":num+"310", "RAIN"])
    rain.append(tor)

#check the correlation between PRCP(precipitation in the end of vegetative) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(rain)
hwah4 = sum_df5.loc[:, 'HWAH'].values

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Precipitation of DAS 70-80 VS Yield", fontsize=18)
plt.xlabel('Precipitation(70-80 days after seeding) (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()















