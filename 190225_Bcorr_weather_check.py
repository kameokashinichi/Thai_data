#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 22:11:57 2019

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
190225 check the B_corr weather scenario.

1. read the B_corr weather data
2. extract the No. of weather scenario which cannot generate crop simulation
3. classify the available and nonavailable weather scenario, then visualize it

Direct-sowing in 18123 -> "2019-02-23T04-46-58-933Z2ceabf44db5dcf78"
Direct-sowing in 18133 -> "2019-02-23T05-24-31-852Zb88764acb3667f91"
Direct-sowing in 18143 -> "2019-02-23T05-24-45-686Z8543f7b824ceba97"
Direct-sowing in 18153 -> "2019-02-23T05-25-07-267Z2d176d027474a535"
Direct-sowing in 18163 -> "2019-02-23T05-25-19-155Zf8045283dc860161"
Direct-sowing in 18173 -> "2019-02-23T05-25-31-011Zaad911c3fb980f06"
Direct-sowing in 18183 -> "2019-02-23T05-25-42-479Z8794f3edc3de886f"
Direct-sowing in 18193 -> "2019-02-23T05-25-53-301Z6c3bdde7c3608348"
Transplanting in 18143 -> "2019-02-23T05-26-03-993Zf834b4268740f7dc"
Transplanting in 18153 -> "2019-02-23T05-26-15-859Z82511d2847cf9854"
Transplanting in 18163 -> "2019-02-23T05-26-26-977Z68682812829185b1"
Transplanting in 18173 -> "2019-02-23T05-26-38-286Z6f85a68c760df954"
Transplanting in 18183 -> "2019-02-23T05-26-50-097Z127a47a1f383e8d5"
Transplanting in 18193 -> "2019-02-23T05-27-00-944Z8d93edca97e5a640"
Transplanting in 18203 -> "2019-02-23T05-27-11-116Z9a9fd16aea7b4eaa"
Transplanting in 18213 -> "2019-02-23T05-27-21-262Zbe3739b479f842bb"
"""

os.mkdir("190225_check_Bcorr_weather_png")

#1. read the B_corr weather data
wlis = list(filter(lambda x: re.search(".WTDE", x), os.listdir("Bias_corrected_WTDE")))
wlis.sort()
WTD = []
for i in range(len(wlis)):
    df = WTD2DataFrame("Bias_corrected_WTDE/"+wlis[i])
    WTD.append(df)

#2. extract the No. of weather scenario which cannot generate crop simulation
ds_id = ["2019-02-23T04-46-58-933Z2ceabf44db5dcf78","2019-02-23T05-24-31-852Zb88764acb3667f91",
         "2019-02-23T05-24-45-686Z8543f7b824ceba97","2019-02-23T05-25-07-267Z2d176d027474a535",
         "2019-02-23T05-25-19-155Zf8045283dc860161","2019-02-23T05-25-31-011Zaad911c3fb980f06",
         "2019-02-23T05-25-42-479Z8794f3edc3de886f","2019-02-23T05-25-53-301Z6c3bdde7c3608348"]

tp_id = ["2019-02-23T05-26-03-993Zf834b4268740f7dc","2019-02-23T05-26-15-859Z82511d2847cf9854",
         "2019-02-23T05-26-26-977Z68682812829185b1","2019-02-23T05-26-38-286Z6f85a68c760df954",
         "2019-02-23T05-26-50-097Z127a47a1f383e8d5","2019-02-23T05-27-00-944Z8d93edca97e5a640",
         "2019-02-23T05-27-11-116Z9a9fd16aea7b4eaa","2019-02-23T05-27-21-262Zbe3739b479f842bb"]

#generate list which consists of the dataframe of Direct-sowing result
dslist = []
dserr = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190223_sskt_cumudata_bias_corr_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
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


#generate list which consists of the dataframe of Transplanting result
tplist = []
tperr = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190223_sskt_cumudata_bias_corr_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
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


#check the amount of rainfall in 100 weather scenarios(from 5/1 to 11/1)
#the columns=['SRAD', 'TMAX', 'TMIN', 'RAIN']
rain = []
for j in range(0, 8):
    rf = []
    for i in range(1,101):
        r = sum(WTD[i-1].iloc[120+10*j:305, 3])
        rf.append(r)
    rf = np.asarray(rf)
    rain.append(rf)


rain[0][np.asarray(dserr[0])-1]

#set bargraph of each scenario(from doy 120)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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

plt.title("General weather scenario -AMOUNT OF RAIN FROM DOY 120 to 300-", fontsize=16)
ax.set_xlabel("Scenario No.", fontsize=15)
ax.set_ylabel("Amount of precipitation from 5/1 to 11/1(mm)", fontsize=15)
#plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY120_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 130)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY130_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 140)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY140_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 150)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY150_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 160)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY160_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 170)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY170_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 180)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY180_300.png", bbox_inches="tight")

plt.show()


#set bargraph of each scenario(from doy 190)
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, len(WTD)+1):
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
#plt.savefig("190225_check_Bcorr_weather_png/190224_general_rain_amount_DOY190_300.png", bbox_inches="tight")

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
            err = err + WTD[j-1].iloc[:365,3].values
            print(j)
        else:
            suc = suc + WTD[j-1].iloc[:365,3].values
    
    if len(dserr[i]) == 0:
        err = err
    else:
        err = err/len(dserr[i])
    suc = suc/(100-len(dserr[i]))
    
    val = np.concatenate((err.reshape(-1, 1), suc.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(val, index=np.arange(1, val.shape[0]+1), 
                      columns=["ERROR", "SUCCEED"])
    
    rain_df.append(df)














