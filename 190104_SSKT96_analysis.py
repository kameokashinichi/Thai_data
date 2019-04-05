#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 15:02:13 2019

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
from matplotlib.patches import Polygon


"""
190104 check the 5 paterns of the dssat simulation.(visualize)
SSKT9601 -> two-time fertilizer with soybean cultivation.(planting date=135)
SSKT9602 -> one-time fertilizer with soybean cultivation.(planting date=135)
SSKT9603 -> one-time fertilizer with soybean cultivation.(planting date=185)
SSKT9604 -> one-time fertilizer with soybean cultivation.(planting date=195)
SSKT9605 -> one-time fertilizer with soybean cultivation.(planting date=205)

dataset is generated in "190103_SSKT96_data_read"
"""
"""
visualize the soil N and yield
1. prepare the list for accumulated day
"""
day = []
for i in range(np.shape(nitro_df1)[0]):
    doy = nitro_df1.iloc[i, 0] + genDaysFromParticularYear(int(nitro_df1.index[i]), 1986)
    day.append(doy)

hdat = []
for i in range(np.shape(sum_df1)[0]):
    doy = 300 + genDaysFromParticularYear(1986+i, 1986)
    hdat.append(doy)

#visualize(SSKT9601, soil_10cm N VS plant growth N)
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

ax.plot(day, nitro_df1["NI2D"].values, color='brown')
ax.plot(day, nitro_df1["NH2D"].values, color='orange')

#ax2.plot(rice_df.index, rice_df.loc[:, 'VNAD'], color='green', label='plant')
#ax2.plot(rice_df.index, rice_df.loc[:, 'GNAD'], color='blue', label='grain')
for i in np.unique(rice_df1["@YEAR"]):
    ax2.plot(rice_df1.index[rice_df1["@YEAR"]==i], 
             rice_df1.loc[:, 'CNAD'][rice_df1["@YEAR"]==i].values, 
             color='red')

soyindex = []
for i in range(np.shape(soy_df1)[0]):
    if soy_df1.iloc[i, 3] == 0:
        soyindex.append(i)
for i in range(len(soyindex)):
    if i == len(soyindex)-1:
        ax2.plot(soy_df1.index[soyindex[i]:len(soy_df1.index)], 
                 soy_df1.iloc[soyindex[i]:len(soy_df1.index), 4].values, 
                 color='green')
    else:
        ax2.plot(soy_df1.index[soyindex[i]:soyindex[i+1]], 
                 soy_df1.iloc[soyindex[i]:soyindex[i+1], 4].values, 
                 color='green')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
rice, = plt.plot((1,2), (2,2), color="red", linewidth=10)
soy, = plt.plot((1,2), (2,2), color="green", linewidth=10)

plt.legend((nh, no, rice, soy), ("Soil NH4-10cm-", "Soil NO3-10cm-", "Rice N", "Soybean N"),
           loc="best", fontsize=14)

plt.title("Soil N content -SSKT9601-", fontsize=18)
plt.xlabel('Day of year from 1986', fontsize=15)
ax.set_ylabel('Soil N content(ppm)', fontsize=15)
ax2.set_ylabel('Plant N content(kg/ha)', fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
ax.set_xlim(100, 1300)
ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190104_soil_10cm_VS_plant_N_SSKT9601.png', bbox_inches='tight')
plt.show()


#visualizeSSKT9601, soil_surface N VS plant growth N with rainfall
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

ax.plot(day, nitro_df1["NI1D"].values, color='brown')
ax.plot(day, nitro_df1["NH1D"].values, color='orange')

#ax2.plot(rice_df.index, rice_df.loc[:, 'VNAD'], color='green', label='plant')
#ax2.plot(rice_df.index, rice_df.loc[:, 'GNAD'], color='blue', label='grain')
for i in np.unique(rice_df1["@YEAR"]):
    ax.plot(rice_df1.index[rice_df1["@YEAR"]==i], 
             rice_df1.loc[:, 'CNAD'][rice_df1["@YEAR"]==i].values, 
             color='red')

soyindex = []
for i in range(np.shape(soy_df1)[0]):
    if soy_df1.iloc[i, 3] == 0:
        soyindex.append(i)
for i in range(len(soyindex)):
    if i == len(soyindex)-1:
        ax.plot(soy_df1.index[soyindex[i]:len(soy_df1.index)], 
                 soy_df1.iloc[soyindex[i]:len(soy_df1.index), 4].values, 
                 color='green')
    else:
        ax.plot(soy_df1.index[soyindex[i]:soyindex[i+1]], 
                 soy_df1.iloc[soyindex[i]:soyindex[i+1], 4].values, 
                 color='green')

acud = np.arange(1, len(sskt.index)+1)
ax2.plot(acud, sskt.loc[:, "RAIN"], color="blue")

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
rice, = plt.plot((1,2), (2,2), color="red", linewidth=10)
soy, = plt.plot((1,2), (2,2), color="green", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, rice, soy, rain), 
           ("Soil NH4-10cm-", "Soil NO3-10cm-", "Rice N", "Soybean N", "rainfall"),
           loc="best", fontsize=14)


plt.title("Soil N content -SSKT9601-", fontsize=18)
plt.xlabel('Day of year from 1986', fontsize=15)
ax.set_ylabel('Soil or Plant N content(kg/ha)', fontsize=15)
ax2.set_ylabel('rainfal amount(mm)', fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
ax.set_xlim(1300, 2500)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190104_soil_surface_VS_plant_N_SSKT9601.png', bbox_inches='tight')
plt.show()


#relation between yield and surface NO3
juv_no1 = nitro_df1.query("130<DOY<150")
uni = []
for i in range(len(juv_no1.index)):
    if i == 0:
        uni.append(i)
    elif juv_no1.index[i] != juv_no1.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no1_uni = juv_no1.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no1_uni["NH1D"].values
hwah4 = sum_df1.loc[:, 'HWAH'].values   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3[:29].reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3[:29], hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NH4 in soil at seedling stage(DAS0) VS Yield", fontsize=18)
plt.xlabel('NH4 content in 10cm layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181224_Dssat_png/190105_NH4_surface_in_DAS0_VS_yield_SSKT9601.png')

plt.show()


#rain fall in the juvenile, vegetative growth season
rain = []
for i in range(0, 31):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    tor = sum(df.loc[num+"260":num+"275", "RAIN"])
    rain.append(tor)

#check the correlation between PRCP(precipitation during juvenile) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(rain)[2:30]
hwah4 = sum_df5.loc[:, 'HWAH'].values[2:]

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
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()


#vixualize the soil N movement in single year(low yield case)
fig = plt.figure(figsize = (12, 6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

dfs = searchElementforX(nitro_df3, '1990')
dfp = rice_df3[rice_df3["@YEAR"] == 1990]
prep = searchElementforX(sskt, '^90')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NI1D'], color='brown')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NH1D'], color='orange')
ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'VNAD'], color='green')
ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'CNAD'], color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax2.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
top, = plt.plot((1,2), (2,2), color="red", linewidth=10)
plant, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, top, plant, rain), ('soil NO3', 'soil NH4', 'plant', 'top', 'rain'),
           loc="best", fontsize=14)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in 1990~low yield in SSKT9603~", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(80, 300)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


#vixualize the soil N movement in single year(high yield case)
fig = plt.figure(figsize = (12, 6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

dfs = searchElementforX(nitro_df3, '2008')
dfp = rice_df3[rice_df3["@YEAR"] == 2008]
prep = searchElementforX(sskt, '^08')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NI1D'], color='brown')
ax.plot(dfs.loc[:, 'DOY'], dfs.loc[:, 'NH1D'], color='orange')
ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'VNAD'], color='green')
ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'CNAD'], color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax2.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
top, = plt.plot((1,2), (2,2), color="red", linewidth=10)
plant, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, top, plant, rain), ('soil NO3', 'soil NH4', 'plant', 'top', 'rain'),
           loc="best", fontsize=14)

nh.set_visible(False)
no.set_visible(False)
top.set_visible(False)
plant.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in 2008(yield="+repr(sum_df3.loc["SSKT0801","HWAH"])+"kg/ha)", 
          fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(100, 350)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_2008_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190105 the correlation between yield and surface NO3(whole simulation)
1. generate two lists(yield and NO3)
"""

#relation between yield and surface NO3
juv_no1 = nitro_df2.query("170<DOY<190")
uni = []
for i in range(len(juv_no1.index)):
    if i == 0:
        uni.append(i)
    elif juv_no1.index[i] != juv_no1.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no1_uni = juv_no1.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no1_uni["NI1D"].values
hwah4 = sum_df2.loc[:, 'HWAH'].values   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3[:29].reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3[:29], hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS35) VS Yield", fontsize=18)
plt.xlabel('NO3 content in surface layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/190105_NO3_surface_in_DAS35_VS_yield_SSKT9602.png')

plt.show()

#SSKT9603, SSKT9604, SSKT9605
juv_no1 = nitro_df5.query("240<DOY<260")
uni = []
for i in range(len(juv_no1.index)):
    if i == 0:
        uni.append(i)
    elif juv_no1.index[i] != juv_no1.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no1_uni = juv_no1.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no1_uni["NI1D"].values
hwah4 = sum_df5.loc[:, 'HWAH'].values   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS35) VS Yield", fontsize=18)
plt.xlabel('NO3 content in surface layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/190105_NO3_surface_in_DAS35_VS_yield_SSKT9605.png')

plt.show()
"""
190105 analyze the outlayer value in SSKT9605
find the factor of the low-yield in Dssat -> compare the weather

sum_df5.sort_values("HWAH")["HWAH"]
"""
#pick up particular year's weather data(RAIN)
fig = plt.figure(figsize = (12, 8))
ax = fig.add_subplot(1,1,1)

hwah = sum_df5["HWAH"].values
n = 0
for i in 1993, 1994, 2005:
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
ax.set_xlim(260, 290)
ax.set_ylim(0, 100)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()





















