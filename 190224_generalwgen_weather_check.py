#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 24 13:24:33 2019

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

['RUNNO', 'TRNO', 'R#', 'O#', 'C#', 'CR', 'MODEL...', 'TNAM.....................', 
'FNAM....', 'WSTA....', 'SOIL_ID...', 'SDAT', 'PDAT', 'EDAT', 'ADAT', 'MDAT', 'HDAT', 
'DWAP', 'CWAM', 'HWAM', 'HWAH', 'BWAH', 'PWAM', 'HWUM', 'H#AM', 'H#UM', 'HIAM', 
'LAIX', 'IR#M', 'IRCM', 'PRCM', 'ETCM', 'EPCM', 'ESCM', 'ROCM', 'DRCM', 'SWXM', 
'NI#M', 'NICM', 'NFXM', 'NUCM', 'NLCM', 'NIAM', 'CNAM', 'GNAM', 'PI#M', 'PICM', 
'PUPC', 'SPAM', 'KI#M', 'KICM', 'KUPC', 'SKAM', 'RECM', 'ONTAM', 'ONAM', 'OPTAM', 
'OPAM', 'OCTAM', 'OCAM', 'DMPPM', 'DMPEM', 'DMPTM', 'DMPIM', 'YPPM', 'YPEM', 
'YPTM', 'YPIM', 'DPNAM', 'DPNUM', 'YPNAM', 'YPNUM', 'NDCH', 'TMAXA', 'TMINA', 
'SRADA', 'DAYLA', 'CO2A', 'PRCP', 'ETCP', 'ESCP', 'EPCP']
190224 check the general weather scenario.

1. read the eujin's weather data
2. extract the No. of weather scenario which cannot generate crop simulation
3. classify the available and nonavailable weather scenario, then visualize it

Direct-sowing in 18123 -> "2019-02-18T06-58-44-229Zf0de45ee989c4be2"
Direct-sowing in 18133 -> "2019-02-18T07-02-46-888Z1b134b4617d1ad9a"
Direct-sowing in 18143 -> "2019-01-10T05-38-16-196Z0dd6e68de7570f4c"
Direct-sowing in 18153 -> "2019-02-18T07-06-42-815Z92560c6b338928d1"
Direct-sowing in 18163 -> "2019-02-18T07-10-47-438Z804a5ab3d565389f"
Direct-sowing in 18173 -> "2019-02-18T07-13-58-272Z5f81b7cb8fac5e2c"
Direct-sowing in 18183 -> "2019-02-18T07-17-40-806Z59ebf8c1d7283ce9"
Direct-sowing in 18193 -> "2019-02-18T07-20-37-052Z97382381cc75e973"
Transplanting in 18193 -> "2019-02-18T07-27-01-220Z15022c8724634e9a"
Transplanting in 18203 -> "2019-02-18T07-29-56-899Z6ad48cbfaea9e270"
Transplanting in 18213 -> "2019-02-18T07-33-01-385Z8ae90b6dc1e2b442"
Transplanting in 18183 -> "2019-02-18T07-36-17-366Z752842139ba27c6c"
Transplanting in 18173 -> "2019-02-18T07-39-16-877Z6c06de3ff36e7614"
Transplanting in 18163 -> "2019-01-10T06-11-52-890Za539c53524cb906e"
Transplanting in 18153 -> "2019-02-18T07-41-56-188Z34aeb7eb0fae960d"
Transplanting in 18143 -> "2019-02-18T07-44-41-332Z92db5dff9619d2cb"
"""

os.mkdir("190224_check_general_weather_png")

#1. read the eujin's weather data
wlis = os.listdir("Weather_file")
wlis.sort()
WTD = []
for i in range(len(wlis)):
    df = WTD2DataFrame("Weather_file/"+wlis[i])
    WTD.append(df)


#2. extract the No. of weather scenario which cannot generate crop simulation
ds_id = ["2019-02-18T06-58-44-229Zf0de45ee989c4be2", "2019-02-18T07-02-46-888Z1b134b4617d1ad9a",
          "2019-01-10T05-38-16-196Z0dd6e68de7570f4c", "2019-02-18T07-06-42-815Z92560c6b338928d1",
          "2019-02-18T07-10-47-438Z804a5ab3d565389f", "2019-02-18T07-13-58-272Z5f81b7cb8fac5e2c",
          "2019-02-18T07-17-40-806Z59ebf8c1d7283ce9", "2019-02-18T07-20-37-052Z97382381cc75e973"]

tp_id = ["2019-02-18T07-44-41-332Z92db5dff9619d2cb", "2019-02-18T07-41-56-188Z34aeb7eb0fae960d",
          "2019-01-10T06-11-52-890Za539c53524cb906e", "2019-02-18T07-39-16-877Z6c06de3ff36e7614",
          "2019-02-18T07-36-17-366Z752842139ba27c6c", "2019-02-18T07-27-01-220Z15022c8724634e9a",
          "2019-02-18T07-29-56-899Z6ad48cbfaea9e270", "2019-02-18T07-33-01-385Z8ae90b6dc1e2b442"]

#direct-sowing
dslist = []
dserr = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190218_cumdata_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    err = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
            if re.search("^2019", rec[15]):
                err.append(i-3)
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
    with open(os.getcwd() + '/190218_cumdata_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    err = []
    for i in range(4, len(record)):
        rec = record[i].split()
        #print(len(rec[15]))
        if len(rec) == 82:
            summary.append(rec)
            if re.search("^2019", rec[15]):
                err.append(i-3)
        else:
            err.append(i-3)
            
    col = record[3].split()[1:]
    #print(col)
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)
    tperr.append(err)


#check the amount of rainfall in 100 weather scenarios(from 5/1 to 11/1)
#the columns=['DAY', 'SRAD', 'TMAX', 'TMIN', 'RAIN']
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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY120_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY130_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY140_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY150_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY160_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY170_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY180_300.png", bbox_inches="tight")

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
#plt.savefig("190224_check_general_weather_png/190224_general_rain_amount_DOY190_300.png", bbox_inches="tight")

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

#eunjin's
rain_df_e = []
for i in range(len(dserr)):
    err = np.zeros(365)
    suc = np.zeros(365)
    for j in range(1, 101):
        if any([x==j for x in dserr[i]]):
            err = err + e_df[e_df.index==j].iloc[:,4].values
            print(j)
        else:
            suc = suc + e_df[e_df.index==j].iloc[:,4].values
    

    if len(dserr[i]) == 0:
        err = err
    else:
        err = err/len(dserr[i])
    suc = suc/(100-len(dserr[i]))
    
    val = np.concatenate((err.reshape(-1, 1), suc.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(val, index=np.arange(1, val.shape[0]+1), 
                      columns=["ERROR", "SUCCEED"])
    
    rain_df_e.append(df)
    
#Actual    
rain_df_a = []
for i in range(len(dserr)):
    err = np.zeros(365)
    suc = np.zeros(365)
    for j in range(1, len(WTD)+1):
        if any([x==j for x in dserr[i]]):
            err = err + WTD[j-1].iloc[:365,3].values
            print(j)
        else:
            suc = suc + WTD[j-1].iloc[:365,3].values
    
    if len(dserr[i]) == 0:
        err = err
    else:
        err = err/len(dserr[i])
    suc = suc/(len(WTD)-len(dserr[i]))
    
    val = np.concatenate((err.reshape(-1, 1), suc.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(val, index=np.arange(1, val.shape[0]+1), 
                      columns=["ERROR", "SUCCEED"])
    
    rain_df_a.append(df)    


#Bcorr
rain_df_b = []
for i in range(len(dserr)):
    err = np.zeros(365)
    suc = np.zeros(365)
    for j in range(1, len(WTD)+1):
        if any([x==j for x in dserr[i]]):
            err = err + WTD[j-1].iloc[:365,3].values
            print(j)
        else:
            suc = suc + WTD[j-1].iloc[:365,3].values
    
    if len(dserr[i]) == 0:
        err = err
    else:
        err = err/len(dserr[i])
    suc = suc/(len(WTD)-len(dserr[i]))
    
    val = np.concatenate((err.reshape(-1, 1), suc.reshape(-1, 1)), axis=1)
    df = pd.DataFrame(val, index=np.arange(1, val.shape[0]+1), 
                      columns=["ERROR", "SUCCEED"])
    
    rain_df_b.append(df) 


#3. compare general, eunjin's and actual
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

ax.plot(np.arange(1, len(rain_df[0].index)+1), rain_df[0]["SUCCEED"].values,
        color="green", linewidth=1)
ax.plot(np.arange(1, len(rain_df_e[0].index)+1), rain_df_e[0]["SUCCEED"].values,
        color="red", linewidth=1)
ax.plot(np.arange(1, len(rain_df_a[0].index)+1), rain_df_a[0]["SUCCEED"].values,
        color="blue", linewidth=1)
ax.plot(np.arange(1, len(rain_df_b[0].index)+1), rain_df_b[0]["SUCCEED"].values,
        color="orange", linewidth=1)

general, = plt.plot([1,1], color="green", linewidth=10)
eunjin, = plt.plot([1,1], color="red", linewidth=10)
actual, = plt.plot([1,1], color="blue", linewidth=10)
bcorr, = plt.plot([1,1], color="orange", linewidth=10)

plt.legend((general, eunjin, actual, bcorr), 
           ("General scenario", "Eunjin's scenario", "Historical weather", "Bias_correction"),
           loc="best", fontsize=14)

general.set_visible(False)
eunjin.set_visible(False)
actual.set_visible(False)

plt.title("General VS Eunjin's VS Historical weather VS bias_corr -DOY 120-300-", fontsize=16)
ax.set_xlabel("Date in 2018", fontsize=15)
ax.set_ylabel("Daily precipitation(mm/day)", fontsize=15)
plt.xticks(np.arange(1, 366, 30), doylist2Date(np.arange(1, 366, 30)))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190224_check_eunjin's_weather_png/190225_General_VS_Eunjin's_VS_ACtual_VS_Bcorr_DOY120_300.png", bbox_inches="tight")

plt.show()


#compare average rainfall of each data

doy = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]

month = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

e_col = []
g_col = []
a_col = []
b_col = []
for i in range(len(doy)):
    if i == 0:
        e = sum(rain_df_e[0].iloc[:doy[i],1])
        g = sum(rain_df[0].iloc[:doy[i],1])
        a = sum(rain_df_a[0].iloc[:doy[i],1])
        b = sum(rain_df_b[0].iloc[:doy[i],1])
    else:
        e = sum(rain_df_e[0].iloc[doy[i-1]:doy[i],1])
        g = sum(rain_df[0].iloc[doy[i-1]:doy[i],1])
        a = sum(rain_df_a[0].iloc[doy[i-1]:doy[i],1])
        b = sum(rain_df_b[0].iloc[doy[i-1]:doy[i],1])        
    e_col.append(e)
    g_col.append(g)
    a_col.append(a)
    b_col.append(b)

arr = np.concatenate((np.asarray(e_col).reshape(-1, 1), np.asarray(g_col).reshape(-1, 1),
                      np.asarray(a_col).reshape(-1, 1), np.asarray(b_col).reshape(-1, 1)),axis=1)

comp_df = pd.DataFrame(arr, index=month, columns=["Eunjin","General","Historical","Bias_corr"])



#bar graph for comparing 3 data
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(len(comp_df.columns)):
    ax.bar(np.arange(1, len(comp_df.index)+1)+n, comp_df.iloc[:, i], width=0.8/len(comp_df.columns),
           label=comp_df.columns[i], color=cm.hsv(i/len(comp_df.columns)))
    
    n = n + 0.8/len(comp_df.columns)

plt.legend(loc="best", fontsize=14)
    
plt.title("General VS Eunjin's VS Historical weather -Monthly Average-", fontsize=16)
ax.set_xlabel("Month in 2018", fontsize=15)
ax.set_ylabel("Monthly precipitation(mm/month)", fontsize=15)
plt.xticks(np.arange(1, len(comp_df.index)+1,1)+0.37, month)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190224_check_eunjin's_weather_png/190224_General_VS_Eunjin's_VS_ACtual_Monthly.png", bbox_inches="tight")

plt.show()


#bar graph for comparing 4 data
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

colors = ["red","green","blue","orange"]

n = 0
for i in range(len(comp_df.columns)):
    ax.bar(np.arange(1, len(comp_df.index)+1)+n, comp_df.iloc[:, i], width=0.8/len(comp_df.columns),
           label=comp_df.columns[i], color=colors[i])
    
    n = n + 0.8/len(comp_df.columns)

plt.legend(loc="best", fontsize=14)
    
plt.title("General VS Eunjin's VS Historical weather VS Bias_corr -Monthly Average-", fontsize=16)
ax.set_xlabel("Month in 2018", fontsize=15)
ax.set_ylabel("Monthly precipitation(mm/month)", fontsize=15)
plt.xticks(np.arange(1, len(comp_df.index)+1,1)+0.37, month)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190224_check_eunjin's_weather_png/190225_General_VS_Eunjin's_VS_ACtual_VS_Bcorr_Monthly.png", bbox_inches="tight")

plt.show()


#compare the error number of each simulation
e_ds = [7,9,11,16,18,26,27,35]
e_tp = [8,10,14,16,22,29,34,41]
g_ds = [0,0,0,0,0,1,2,4]
g_tp = [0,0,0,0,0,0,3,8]
a_ds = [0,0,0,0,1,1,1,3]
a_tp = [0,0,0,0,1,1,1,3]
b_ds = [0,0,0,0,1,1,4,10]
b_tp = [0,0,0,1,1,3,6,10]

err_val = np.concatenate((np.asarray(e_ds).reshape(-1,1),np.asarray(e_tp).reshape(-1,1),
                          np.asarray(g_ds).reshape(-1,1),np.asarray(g_tp).reshape(-1,1),
                          np.asarray(a_ds).reshape(-1,1),np.asarray(a_tp).reshape(-1,1),
                          np.asarray(b_ds).reshape(-1,1),np.asarray(b_tp).reshape(-1,1)), axis=1)

err_df = pd.DataFrame(err_val, index=["5/3","5/13","5/23","6/2","6/12","6/22","7/2","7/12"],
                      columns=["Eunjin_ds","Eunjin_tp","General_ds",
                               "General_tp","Historical_ds","Historical_tp",
                               "Bcorr_ds","Bcorr_tp"])

#bar graph for the number of error
fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(len(err_df.columns)):
    ax.bar(np.arange(1, len(err_df.index)+1)+n, err_df.iloc[:, i], width=0.8/len(err_df.columns),
           label=err_df.columns[i], color=cm.hsv(i/len(err_df.columns)))
    
    n = n + 0.8/len(err_df.columns)

plt.legend(loc="best", fontsize=14)
    
plt.title("General VS Eunjin's VS Historical weather -The number of error-", fontsize=18)
ax.set_xlabel("The date of seeding", fontsize=16)
ax.set_ylabel("The number of error simulation", fontsize=16)
plt.xticks(np.arange(1, len(err_df.index)+1,1)+0.37, err_df.index)
plt.setp(ax.get_xticklabels(), fontsize=16, rotation=30, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=16, visible=True)
plt.savefig("190224_check_eunjin's_weather_png/190225_General_VS_Eunjin's_VS_ACtual_VS_Bcorr_ErrorNum.png", bbox_inches="tight")

plt.show()






