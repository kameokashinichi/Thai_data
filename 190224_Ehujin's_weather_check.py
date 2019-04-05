#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 10:10:44 2019

@author: kameokashinichi
"""

import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math
from statistics import mean, stdev
import matplotlib.cm as cm

"""
190224 check the eunjin's weather scenario.

1. read the eujin's weather data
2. extract the No. of weather scenario which cannot generate crop simulation
3. classify the available and nonavailable weather scenario, then visualize it

Direct-sowing in 18123 -> "2019-02-21T07-18-59-907Z8ca056028d852761"
Direct-sowing in 18133 -> "2019-02-21T07-16-51-918Zab8cbd36703a71a9"
Direct-sowing in 18143 -> "2019-02-21T07-14-38-131Z9c6c0d47bcb8d823"
Direct-sowing in 18153 -> "2019-02-21T07-12-23-049Z1ed6c1a27f6f7106"
Direct-sowing in 18163 -> "2019-02-21T07-10-17-800Z50b4bb45fb91b51c"
Direct-sowing in 18173 -> "2019-02-21T07-04-05-717Z71fcb99abbb80387"
Direct-sowing in 18183 -> "2019-02-21T07-01-51-211Z6d10fc229ab89f61"
Direct-sowing in 18193 -> "2019-02-21T06-58-38-398Z1fb6f925943252be"
Transplanting in 18193 -> "2019-02-21T06-49-59-993Z34cfbaa827cec0bf"
Transplanting in 18203 -> "2019-02-21T06-52-58-744Z2c702ca536957b38"
Transplanting in 18213 -> "2019-02-21T06-55-44-838Ze0aaed306ef5c16d"
Transplanting in 18183 -> "2019-02-21T06-47-43-089Z79e1e454893c56be"
Transplanting in 18173 -> "2019-02-21T06-45-06-478Z892c4c8494ae6fb5"
Transplanting in 18163 -> "2019-02-21T06-40-43-004Z4f371926b5b25541"
Transplanting in 18153 -> "2019-02-21T06-37-38-207Za760c71f8d4bfe28"
Transplanting in 18143 -> "2019-02-21T06-33-56-126Z642e638052eccfb6"
"""

os.mkdir("190224_check_eunjin's_weather_png")

#1.read the eujin's weather data
WTD = []
with open("WGEN_out_SRIS.txt") as f:
#print(type(f))
    for row in f:
    #print(type(row))
        WTD.append(row.strip())

print("start separating")        
weather = []
for row in WTD:
    element = row.split()
    weather.append(element)

print("start appending")
#weather[0] = weather[0][1:]
weather = np.asarray(weather)
ind = weather[1:, 0].astype(np.int32)
#print(weather[0])
e_df = pd.DataFrame(weather[1:, 1:].astype(np.float32), index=ind, columns=["DAY", "SRAD", "TMAX", "TMIN", "RAIN"])


#2. extract the No. of weather scenario which cannot generate crop simulation
ds_id = ["2019-02-21T07-18-59-907Z8ca056028d852761", "2019-02-21T07-16-51-918Zab8cbd36703a71a9",
          "2019-02-21T07-14-38-131Z9c6c0d47bcb8d823", "2019-02-21T07-12-23-049Z1ed6c1a27f6f7106",
          "2019-02-21T07-10-17-800Z50b4bb45fb91b51c", "2019-02-21T07-04-05-717Z71fcb99abbb80387",
          "2019-02-21T07-01-51-211Z6d10fc229ab89f61", "2019-02-21T06-58-38-398Z1fb6f925943252be"]

tp_id = ["2019-02-21T06-33-56-126Z642e638052eccfb6", "2019-02-21T06-37-38-207Za760c71f8d4bfe28",
          "2019-02-21T06-40-43-004Z4f371926b5b25541", "2019-02-21T06-45-06-478Z892c4c8494ae6fb5",
          "2019-02-21T06-47-43-089Z79e1e454893c56be", "2019-02-21T06-49-59-993Z34cfbaa827cec0bf",
          "2019-02-21T06-52-58-744Z2c702ca536957b38", "2019-02-21T06-55-44-838Ze0aaed306ef5c16d"]

#direct-sowing
dslist = []
dserr = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190221_sskt_cumudata_eunjin_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    err = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
        else:
            err.append(i-3)
    
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    dslist.append(df)
    dserr.append(err)


#Transplanting
tplist = []
tperr = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190221_sskt_cumudata_eunjin_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    err = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
        else:
            err.append(i-3)
            
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)
    tperr.append(err)


    
#3. classify the available and nonavailable weather scenario, then visualize it    
#-RAIN-
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[0]]):
        ax.plot(e_df[e_df.index == i]["DAY"].values, e_df[e_df.index == i]["RAIN"].values,
                color="blue", linewidth=0.5)
#    else:
#        ax.plot(e_df[e_df.index == i]["DAY"].values, e_df[e_df.index == i]["RAIN"].values,
#                color="red", linewidth=0.5)

error, = plt.plot([1,1], color="blue", linewidth=10)
#succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
#succeed.set_visible(False)

plt.title("Eunjin's weather scenario -RAIN-", fontsize=16)
ax.set_xlabel("Date in 2018", fontsize=15)
ax.set_ylabel("Daily precipitation(mm/day)", fontsize=15)
plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=12, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=12, visible=True)

plt.show()

"""
190224 compare the average rainfall of Succeed and Error

1. calculate the daily average of each dataset
2. prepare dataframe for each average daily rainfall
3. visualize by two line(average of succeed and error)
"""

#1. calculate the daily average of each dataset
#2. prepare dataframe for each average daily rainfall
rain_df = []
for i in range(len(dserr)):
    err = np.zeros(365)
    suc = np.zeros(365)
    for j in range(1, 101):
        if any([x==j for x in dserr[i]]):
            err = err + e_df[e_df.index==j].iloc[:,4].values
            print(j)
        else:
            suc = suc + e_df[e_df.index==j].iloc[:,4].values
    

    err = err/len(dserr[i])
    suc = suc/(100-len(dserr[i]))
    
    val = np.concatenate((err.reshape(-1, 1), suc.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(val, index=np.arange(1, val.shape[0]+1), 
                      columns=["ERROR", "SUCCEED"])
    
    rain_df.append(df)


#3. visualize by two line(average of succeed and error)(DOY120)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

ax.plot(np.arange(1, len(rain_df[0].index)+1), rain_df[0]["ERROR"].values,
        color="blue", linewidth=2)

ax.plot(np.arange(1, len(rain_df[0].index)+1), rain_df[0]["SUCCEED"].values,
        color="red", linewidth=2)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("Eunjin's weather scenario -DAILY RAIN ERROR VS SUCCEED DOY 120-300-", fontsize=16)
ax.set_xlabel("Date in 2018", fontsize=15)
ax.set_ylabel("Daily precipitation(mm/day)", fontsize=15)
plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_errorVSsucceed_DOY120_300.png", bbox_inches="tight")

plt.show()



#3. visualize by two line(average of succeed and error)(DOY130)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

ax.plot(np.arange(1, len(rain_df[7].index)+1), rain_df[7]["ERROR"].values,
        color="blue", linewidth=2)

ax.plot(np.arange(1, len(rain_df[7].index)+1), rain_df[7]["SUCCEED"].values,
        color="red", linewidth=2)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("Eunjin's weather scenario -DAILY RAIN ERROR VS SUCCEED DOY 130-300-", fontsize=16)
ax.set_xlabel("Date in 2018", fontsize=15)
ax.set_ylabel("Daily precipitation(mm/day)", fontsize=15)
plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_errorVSsucceed_DOY130_300.png", bbox_inches="tight")

plt.show()



#check the amount of rainfall in 100 weather scenarios(from 5/1 to 11/1)
#the columns=['DAY', 'SRAD', 'TMAX', 'TMIN', 'RAIN']
rain = []
for j in range(0, 8):
    rf = []
    for i in range(1,101):
        r = sum(e_df[e_df.index==i].iloc[120+10*j:305, 4])
        rf.append(r)
    rf = np.asarray(rf)
    rain.append(rf)


rain[0][np.asarray(dserr[0])-1]



"""
Set the amount of rainfall in designated duration
"""

#set bargraph of each scenario(from doy 120)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[0]]):
        ax.bar(i, rain[0][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[0][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("Eunjin's weather scenario -AMOUNT OF RAIN FROM DOY 120 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 5/1 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY120_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 130)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[1]]):
        ax.bar(i, rain[1][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[1][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 130 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 5/11 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY130_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 140)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[2]]):
        ax.bar(i, rain[2][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[2][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 140 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 5/21 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY140_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 150)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[3]]):
        ax.bar(i, rain[3][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[3][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 150 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 5/31 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY150_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 160)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[4]]):
        ax.bar(i, rain[4][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[4][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 160 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 6/10 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY160_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 170)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[5]]):
        ax.bar(i, rain[5][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[5][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 170 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 6/20 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY170_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 180)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[6]]):
        ax.bar(i, rain[6][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[6][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 180 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 6/30 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY180_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 190)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in np.unique(e_df.index):
    if any([x == i for x in dserr[7]]):
        ax.bar(i, rain[7][i-1], color="blue", width=0.8)
    else:
        ax.bar(i, rain[7][i-1], color="red", width=0.8)

error, = plt.plot([1,1], color="blue", linewidth=10)
succeed, = plt.plot([1,1], color="red", linewidth=10)

plt.legend((error, succeed), ("Error scenario", "Succeed scenario"), 
           loc="best", fontsize=14)

error.set_visible(False)
succeed.set_visible(False)

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 190 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 7/2 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_Eunjin's_rain_amount_DOY190_300.png", bbox_inches="tight")

plt.show()















