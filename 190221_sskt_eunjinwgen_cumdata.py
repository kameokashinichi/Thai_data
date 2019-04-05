#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 11:31:25 2019

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
import requests
import json
import subprocess


"""
190221 convert .txt file into .WTDE and .WTH respectively

1. generate folder for the weather files
2. devide the .txt file from Eunjin into 100 weather files
    ・convert header from " IYear DoY  SRAD   TMAX   TMIN   RAIN " into "@  DATE  SRAD  TMAX  TMIN  RAIN  TAVE"
3  generate 100 "COMM00xx.WTDE file by using dataframe2wtd function
4. generate 100 "00xx1801.WTH" file by using "gencli.a" and "genWTH.a" via subprocess module
5. store these data into one directory
"""

#1. generate the folder for the weather files
os.mkdir("weather_file_SSKT_Eunjin")

#2. devide the .txt file from Eunjin 'WGEN_out_SRIS.txt' into 100 weather files
#convert into pandas.DataFrame
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
ind = weather[1:, 0]
#print(weather[0])
df = pd.DataFrame(weather[1:, 1:].astype(np.float32), index=ind, columns=["DAY", "SRAD", "TMAX", "TMIN", "RAIN"])

year = pd.DataFrame(np.repeat(2018, len(df.index)), index=ind, columns=["YEAR"])

df = pd.concat([df, year], axis=1)

#devide into annual weather data by using index
#3. generate 100 "COMM00xx.WTDE file by using dataframe2wtd function
for i in range(1, 101):
    anu = df[df.index == repr(i)]
    dataframe2wtd(anu, "weather_file_SSKT_Eunjin/COMM"+repr(i).zfill(4), add_tave=True, to_slice=False, to_check=True, out_extension = ".WTDE")

#4. generate 100 "00xx1801.WTH" file by using "gencli.a" and "genWTH.a" via subprocess module
#5. store these data into one directory
for i in range(1, 101):
    #os.chdir("/Users/kameokashinichi/Documents/postdoc/crop_util")
    
    subprocess.call(["./genCLI.a", "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/weather_file_SSKT_Eunjin/COMM"+repr(i).zfill(4)+".WTDE",
                     repr(i).zfill(4), "15.000", "104.050", "4"])
    subprocess.call(["./genWTH.a", repr(i).zfill(4)+".CLI", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/weather_file_SSKT_Eunjin/COMM"+repr(i).zfill(4)+".WTDE"])
    subprocess.call(["mv", repr(i).zfill(4)+"1801.WTH", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/weather_file_SSKT_Eunjin/"])
    subprocess.call(["mv", repr(i).zfill(4)+".CLI", 
                     "./eunjin_cli/"])
    
    #os.chdir("/Users/kameokashinichi/Documents/postdoc/listenfield/Seasonal_forecast_influence_test/weather_file"+repr(year)+"/")


"""
190221 check the accuracy of the wgen made by eunjin

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

ds_id = ["2019-02-21T07-18-59-907Z8ca056028d852761", "2019-02-21T07-16-51-918Zab8cbd36703a71a9",
          "2019-02-21T07-14-38-131Z9c6c0d47bcb8d823", "2019-02-21T07-12-23-049Z1ed6c1a27f6f7106",
          "2019-02-21T07-10-17-800Z50b4bb45fb91b51c", "2019-02-21T07-04-05-717Z71fcb99abbb80387",
          "2019-02-21T07-01-51-211Z6d10fc229ab89f61", "2019-02-21T06-58-38-398Z1fb6f925943252be"]

tp_id = ["2019-02-21T06-33-56-126Z642e638052eccfb6", "2019-02-21T06-37-38-207Za760c71f8d4bfe28",
          "2019-02-21T06-40-43-004Z4f371926b5b25541", "2019-02-21T06-45-06-478Z892c4c8494ae6fb5",
          "2019-02-21T06-47-43-089Z79e1e454893c56be", "2019-02-21T06-49-59-993Z34cfbaa827cec0bf",
          "2019-02-21T06-52-58-744Z2c702ca536957b38", "2019-02-21T06-55-44-838Ze0aaed306ef5c16d"]


#os.mkdir("190221_sskt_cumudata_eunjin_wgen")

#generate list which consists of the dataframe of Direct-sowing result
dslist = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190221_sskt_cumudata_eunjin_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
    
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    dslist.append(df)


#generate list which consists of the dataframe of Transplanting result
tplist = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190221_sskt_cumudata_eunjin_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
    
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)

#make directory
os.mkdir("190221_sskt_eunjinwgen_yield_png")

#compare these two ~tpdate == 18123~
order0 = dslist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[0], ord_df0], axis=1, sort=True)
order1 = tplist[0].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[0], ord_df1], axis=1, sort=True)

val0 = dslist[0]['HWAH'].values.astype(np.float32)
val1 = tplist[0]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

#yy1_0 = float(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)]),'HWAH'])*0.7
yy2_0 = float(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[0].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[0].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[0].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[0].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
ax.set_xlim(2500, 6000)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index)+5)
#ax2.set_ylim(0, len(sum_ds1.index)+5)
#plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18123_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18133~
order0 = dslist[1].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[1].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[1]['HWAH'].values.astype(np.float32)
val1 = tplist[1]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[1].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[1].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[1].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[1].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 6000)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18133_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the late May~
order0 = dslist[2].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[2], ord_df0], axis=1, sort=True)
order1 = tplist[2].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[2], ord_df1], axis=1, sort=True)

val0 = dslist[2]['HWAH'].values.astype(np.float32)
val1 = tplist[2]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[2].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[2].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[2].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[2].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 6000)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18143_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the early June~
order0 = dslist[3].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[3], ord_df0], axis=1, sort=True)
order1 = tplist[3].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[3], ord_df1], axis=1, sort=True)

val0 = dslist[3]['HWAH'].values.astype(np.float32)
val1 = tplist[3]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[3].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[3].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[3].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[3].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2000, 5500)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18153_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle June~
order0 = dslist[4].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[4], ord_df0], axis=1, sort=True)
order1 = tplist[4].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[4], ord_df1], axis=1, sort=True)

val0 = dslist[4]['HWAH'].values.astype(np.float32)
val1 = tplist[4]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[4].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[4].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[4].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[4].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 99, 9).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 100, 9).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 5500)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18163_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the late June~
order0 = dslist[5].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[5], ord_df0], axis=1, sort=True)
order1 = tplist[5].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[5], ord_df1], axis=1, sort=True)

val0 = dslist[5]['HWAH'].values.astype(np.float32)
val1 = tplist[5]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[5].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[5].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[5].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[5].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 95, 8).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 99, 8).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 5000)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18173_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the early July~
order0 = dslist[6].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[6], ord_df0], axis=1, sort=True)
order1 = tplist[6].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[6], ord_df1], axis=1, sort=True)

val0 = dslist[6]['HWAH'].values.astype(np.float32)
val1 = tplist[6]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[6].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[6].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[6].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[6].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 95, 8).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 92, 7).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4500)
#plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18183_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle July~
order0 = dslist[7].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[7], ord_df0], axis=1, sort=True)
order1 = tplist[7].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[7], ord_df1], axis=1, sort=True)

val0 = dslist[7]['HWAH'].values.astype(np.float32)
val1 = tplist[7]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2500

yy1_0 = float(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[7].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[7].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[7].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[7].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_EUNJIN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 92, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 100, 7).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4500)
plt.savefig("190221_sskt_eunjinwgen_yield_png/190221_CDF_Reiton_Yield_TP_VS_DS_18193_WGEN_EUNJIN.png", bbox_inches='tight')

plt.show()


"""
#MATURITY DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190222_sskt_eunjinwgen_mdat_png")

order0=dslist[0].sort_values("MDAT").index
order1=tplist[0].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[0].index)+1):
    if dslist[0]['MDAT'][i] < 2019000:
        val = dslist[0]['MDAT'][i] - 2018000
    else:
        val = dslist[0]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[0].index)+1):
    if tplist[0]['MDAT'][i] < 2019000:
        val = tplist[0]['MDAT'][i] - 2018000
    else:
        val = tplist[0]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[0].index)*0.2
val50_0 = len(dslist[0].index)*0.5
val80_0 = len(dslist[0].index)*0.8
val20_1 = len(tplist[0].index)*0.2
val50_1 = len(tplist[0].index)*0.5
val80_1 = len(tplist[0].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(20*len(dslist[0].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(50*len(dslist[0].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(80*len(dslist[0].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(20*len(tplist[0].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(50*len(tplist[0].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(80*len(tplist[0].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(280, 340, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(280, 340, 10)))
ax.set_yticklabels(np.linspace(0, round(10000/len(order0)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(order1)), 6).astype(np.int32))
ax.set_xlim(280, 330)
ax2.set_xlim(280, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate123.png", bbox_inches='tight')
plt.show()


#Maturity date in 18133
order0=dslist[1].sort_values("MDAT").index
order1=tplist[1].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[1].index)+1):
    if dslist[1]['MDAT'][i] < 2019000:
        val = dslist[1]['MDAT'][i] - 2018000
    else:
        val = dslist[1]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[1].index)+1):
    if tplist[1]['MDAT'][i] < 2019000:
        val = tplist[1]['MDAT'][i] - 2018000
    else:
        val = tplist[1]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[1].index)*0.2
val50_0 = len(dslist[1].index)*0.5
val80_0 = len(dslist[1].index)*0.8
val20_1 = len(tplist[1].index)*0.2
val50_1 = len(tplist[1].index)*0.5
val80_1 = len(tplist[1].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(20*len(dslist[1].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(50*len(dslist[1].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(80*len(dslist[1].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(20*len(tplist[1].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(50*len(tplist[1].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(80*len(tplist[1].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax.set_yticklabels(np.linspace(0, round(10000/len(order0)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(order1)), 6).astype(np.int32))
ax.set_xlim(290, 340)
ax2.set_xlim(290, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate133.png", bbox_inches='tight')
plt.show()


#Maturity date in 18143
order0=dslist[2].sort_values("MDAT").index
order1=tplist[2].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[2].index)+1):
    if dslist[2]['MDAT'][i] < 2019000:
        val = dslist[2]['MDAT'][i] - 2018000
    else:
        val = dslist[2]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[2].index)+1):
    if tplist[2]['MDAT'][i] < 2019000:
        val = tplist[2]['MDAT'][i] - 2018000
    else:
        val = tplist[2]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[2].index)*0.2
val50_0 = len(dslist[2].index)*0.5
val80_0 = len(dslist[2].index)*0.8
val20_1 = len(tplist[2].index)*0.2
val50_1 = len(tplist[2].index)*0.5
val80_1 = len(tplist[2].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(20*len(dslist[2].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(50*len(dslist[2].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(80*len(dslist[2].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(20*len(tplist[2].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(50*len(tplist[2].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(80*len(tplist[2].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax.set_yticklabels(np.linspace(0, round(10000/len(order0)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(order1)), 6).astype(np.int32))
ax.set_xlim(290, 340)
ax2.set_xlim(290, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate143.png", bbox_inches='tight')
plt.show()


#Maturity date in 18153
order0=dslist[3].sort_values("MDAT").index
order1=tplist[3].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[3].index)+1):
    if dslist[3]['MDAT'][i] < 2019000:
        val = dslist[3]['MDAT'][i] - 2018000
    else:
        val = dslist[3]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[3].index)+1):
    if tplist[3]['MDAT'][i] < 2019000:
        val = tplist[3]['MDAT'][i] - 2018000
    else:
        val = tplist[3]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[3].index)*0.2
val50_0 = len(dslist[3].index)*0.5
val80_0 = len(dslist[3].index)*0.8
val20_1 = len(tplist[3].index)*0.2
val50_1 = len(tplist[3].index)*0.5
val80_1 = len(tplist[3].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(20*len(dslist[3].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(50*len(dslist[3].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(80*len(dslist[3].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(20*len(tplist[3].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(50*len(tplist[3].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(80*len(tplist[3].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(300, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(300, 345, 5)))
ax.set_yticklabels(np.linspace(0, 100, 9).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 100, 9).astype(np.int32))
ax.set_xlim(300, 340)
ax2.set_xlim(300, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate153.png", bbox_inches='tight')
plt.show()


#Maturity date in 18163
order0=dslist[4].sort_values("MDAT").index
order1=tplist[4].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[4].index)+1):
    if dslist[4]['MDAT'][i] < 2019000:
        val = dslist[4]['MDAT'][i] - 2018000
    else:
        val = dslist[4]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[4].index)+1):
    if tplist[4]['MDAT'][i] < 2019000:
        val = tplist[4]['MDAT'][i] - 2018000
    else:
        val = tplist[4]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[4].index)*0.2
val50_0 = len(dslist[4].index)*0.5
val80_0 = len(dslist[4].index)*0.8
val20_1 = len(tplist[4].index)*0.2
val50_1 = len(tplist[4].index)*0.5
val80_1 = len(tplist[4].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(20*len(dslist[4].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(50*len(dslist[4].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(80*len(dslist[4].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(20*len(tplist[4].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(50*len(tplist[4].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(80*len(tplist[4].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(305, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(305, 345, 5)))
ax.set_yticklabels(np.linspace(0, 99, 9).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 102, 9).astype(np.int32))
ax.set_xlim(305, 340)
ax2.set_xlim(305, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate163.png", bbox_inches='tight')
plt.show()


#Maturity date in 18173
order0=dslist[5].sort_values("MDAT").index
order1=tplist[5].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[5].index)+1):
    if dslist[5]['MDAT'][i] < 2019000:
        val = dslist[5]['MDAT'][i] - 2018000
    else:
        val = dslist[5]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[5].index)+1):
    if tplist[5]['MDAT'][i] < 2019000:
        val = tplist[5]['MDAT'][i] - 2018000
    else:
        val = tplist[5]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[5].index)*0.2
val50_0 = len(dslist[5].index)*0.5
val80_0 = len(dslist[5].index)*0.8
val20_1 = len(tplist[5].index)*0.2
val50_1 = len(tplist[5].index)*0.5
val80_1 = len(tplist[5].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(20*len(dslist[5].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(50*len(dslist[5].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(80*len(dslist[5].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(20*len(tplist[5].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(50*len(tplist[5].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(80*len(tplist[5].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(310, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(310, 345, 5)))
ax.set_yticklabels(np.linspace(0, 96, 8).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 100, 8).astype(np.int32))
ax.set_xlim(310, 340)
ax2.set_xlim(310, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate173.png", bbox_inches='tight')
plt.show()


#Maturity date in 18183
order0=dslist[6].sort_values("MDAT").index
order1=tplist[6].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[6].index)+1):
    if dslist[6]['MDAT'][i] < 2019000:
        val = dslist[6]['MDAT'][i] - 2018000
    else:
        val = dslist[6]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[6].index)+1):
    if tplist[6]['MDAT'][i] < 2019000:
        val = tplist[6]['MDAT'][i] - 2018000
    else:
        val = tplist[6]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[6].index)*0.2
val50_0 = len(dslist[6].index)*0.5
val80_0 = len(dslist[6].index)*0.8
val20_1 = len(tplist[6].index)*0.2
val50_1 = len(tplist[6].index)*0.5
val80_1 = len(tplist[6].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(20*len(dslist[6].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(50*len(dslist[6].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(80*len(dslist[6].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(20*len(tplist[6].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(50*len(tplist[6].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(80*len(tplist[6].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax.set_yticklabels(np.linspace(0, 97, 8).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 7).astype(np.int32))
ax.set_xlim(315, 340)
ax2.set_xlim(315, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate183.png", bbox_inches='tight')
plt.show()


#Maturity date in 18193
order0=dslist[7].sort_values("MDAT").index
order1=tplist[7].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[7].index)+1):
    if dslist[7]['MDAT'][i] < 2019000:
        val = dslist[7]['MDAT'][i] - 2018000
    else:
        val = dslist[7]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[7].index)+1):
    if tplist[7]['MDAT'][i] < 2019000:
        val = tplist[7]['MDAT'][i] - 2018000
    else:
        val = tplist[7]['MDAT'][i] - 2019000+365
    mdat1.append(val)

val20_0 = len(dslist[7].index)*0.2
val50_0 = len(dslist[7].index)*0.5
val80_0 = len(dslist[7].index)*0.8
val20_1 = len(tplist[7].index)*0.2
val50_1 = len(tplist[7].index)*0.5
val80_1 = len(tplist[7].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(20*len(dslist[7].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(50*len(dslist[7].index)/100)],'MDAT']-2018000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(80*len(dslist[7].index)/100)],'MDAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(20*len(tplist[7].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(50*len(tplist[7].index)/100)],'MDAT']-2018000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(80*len(tplist[7].index)/100)],'MDAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax.set_yticklabels(np.linspace(0, 90, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 85, 6).astype(np.int32))
ax.set_xlim(315, 340)
ax2.set_xlim(315, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_mdat_png/190222_CDF_SSKT_WgenEunjin_Maturity_pdate193.png", bbox_inches='tight')
plt.show()


"""
#ANTHESIS DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190222_sskt_eunjinwgen_adat_png")

order0=dslist[0].sort_values("ADAT").index
order1=tplist[0].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[0].index)+1):
    if dslist[0]['ADAT'][i] < 2019000:
        val = dslist[0]['ADAT'][i] - 2018000
    else:
        val = dslist[0]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[0].index)+1):
    if tplist[0]['ADAT'][i] < 2019000:
        val = tplist[0]['ADAT'][i] - 2018000
    else:
        val = tplist[0]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[0].index)*0.2
val50_0 = len(dslist[0].index)*0.5
val80_0 = len(dslist[0].index)*0.8
val20_1 = len(tplist[0].index)*0.2
val50_1 = len(tplist[0].index)*0.5
val80_1 = len(tplist[0].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(20*len(dslist[0].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(50*len(dslist[0].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(80*len(dslist[0].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(20*len(tplist[0].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(50*len(tplist[0].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(80*len(tplist[0].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Wgen-", fontsize=18)
ax2.set_xlabel("The anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 85, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 85, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate123.png", bbox_inches='tight')
plt.show()


#Maturity date in 18133
order0=dslist[1].sort_values("ADAT").index
order1=tplist[1].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[1].index)+1):
    if dslist[1]['ADAT'][i] < 2019000:
        val = dslist[1]['ADAT'][i] - 2018000
    else:
        val = dslist[1]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[1].index)+1):
    if tplist[1]['ADAT'][i] < 2019000:
        val = tplist[1]['ADAT'][i] - 2018000
    else:
        val = tplist[1]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[1].index)*0.2
val50_0 = len(dslist[1].index)*0.5
val80_0 = len(dslist[1].index)*0.8
val20_1 = len(tplist[1].index)*0.2
val50_1 = len(tplist[1].index)*0.5
val80_1 = len(tplist[1].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(20*len(dslist[1].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(50*len(dslist[1].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(80*len(dslist[1].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(20*len(tplist[1].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(50*len(tplist[1].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(80*len(tplist[1].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 84, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 84, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate133.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18143
order0=dslist[2].sort_values("ADAT").index
order1=tplist[2].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[2].index)+1):
    if dslist[2]['ADAT'][i] < 2019000:
        val = dslist[2]['ADAT'][i] - 2018000
    else:
        val = dslist[2]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[2].index)+1):
    if tplist[2]['ADAT'][i] < 2019000:
        val = tplist[2]['ADAT'][i] - 2018000
    else:
        val = tplist[2]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[2].index)*0.2
val50_0 = len(dslist[2].index)*0.5
val80_0 = len(dslist[2].index)*0.8
val20_1 = len(tplist[2].index)*0.2
val50_1 = len(tplist[2].index)*0.5
val80_1 = len(tplist[2].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(20*len(dslist[2].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(50*len(dslist[2].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(80*len(dslist[2].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(20*len(tplist[2].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(50*len(tplist[2].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(80*len(tplist[2].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 88, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 92, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate143.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18153
order0=dslist[3].sort_values("ADAT").index
order1=tplist[3].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[3].index)+1):
    if dslist[3]['ADAT'][i] < 2019000:
        val = dslist[3]['ADAT'][i] - 2018000
    else:
        val = dslist[3]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[3].index)+1):
    if tplist[3]['ADAT'][i] < 2019000:
        val = tplist[3]['ADAT'][i] - 2018000
    else:
        val = tplist[3]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[3].index)*0.2
val50_0 = len(dslist[3].index)*0.5
val80_0 = len(dslist[3].index)*0.8
val20_1 = len(tplist[3].index)*0.2
val50_1 = len(tplist[3].index)*0.5
val80_1 = len(tplist[3].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(20*len(dslist[3].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(50*len(dslist[3].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(80*len(dslist[3].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(20*len(tplist[3].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(50*len(tplist[3].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(80*len(tplist[3].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 94, 9).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 94, 9).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate153.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18163
order0=dslist[4].sort_values("ADAT").index
order1=tplist[4].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[4].index)+1):
    if dslist[4]['ADAT'][i] < 2019000:
        val = dslist[4]['ADAT'][i] - 2018000
    else:
        val = dslist[4]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[4].index)+1):
    if tplist[4]['ADAT'][i] < 2019000:
        val = tplist[4]['ADAT'][i] - 2018000
    else:
        val = tplist[4]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[4].index)*0.2
val50_0 = len(dslist[4].index)*0.5
val80_0 = len(dslist[4].index)*0.8
val20_1 = len(tplist[4].index)*0.2
val50_1 = len(tplist[4].index)*0.5
val80_1 = len(tplist[4].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(20*len(dslist[4].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(50*len(dslist[4].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(80*len(dslist[4].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(20*len(tplist[4].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(50*len(tplist[4].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(80*len(tplist[4].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 86, 8).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 8).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate163.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18173
order0=dslist[5].sort_values("ADAT").index
order1=tplist[5].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[5].index)+1):
    if dslist[5]['ADAT'][i] < 2019000:
        val = dslist[5]['ADAT'][i] - 2018000
    else:
        val = dslist[5]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[5].index)+1):
    if tplist[5]['ADAT'][i] < 2019000:
        val = tplist[5]['ADAT'][i] - 2018000
    else:
        val = tplist[5]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[5].index)*0.2
val50_0 = len(dslist[5].index)*0.5
val80_0 = len(dslist[5].index)*0.8
val20_1 = len(tplist[5].index)*0.2
val50_1 = len(tplist[5].index)*0.5
val80_1 = len(tplist[5].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(20*len(dslist[5].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(50*len(dslist[5].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(80*len(dslist[5].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(20*len(tplist[5].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(50*len(tplist[5].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(80*len(tplist[5].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, 340, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, 340, 10)))
ax.set_yticklabels(np.linspace(0, 81, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 85, 7).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate173.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18183
order0=dslist[6].sort_values("ADAT").index
order1=tplist[6].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[6].index)+1):
    if dslist[6]['ADAT'][i] < 2019000:
        val = dslist[6]['ADAT'][i] - 2018000
    else:
        val = dslist[6]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[6].index)+1):
    if tplist[6]['ADAT'][i] < 2019000:
        val = tplist[6]['ADAT'][i] - 2018000
    else:
        val = tplist[6]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[6].index)*0.2
val50_0 = len(dslist[6].index)*0.5
val80_0 = len(dslist[6].index)*0.8
val20_1 = len(tplist[6].index)*0.2
val50_1 = len(tplist[6].index)*0.5
val80_1 = len(tplist[6].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(20*len(dslist[6].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(50*len(dslist[6].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(80*len(dslist[6].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(20*len(tplist[6].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(50*len(tplist[6].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(80*len(tplist[6].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, 320, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, 330, 5)))
ax.set_yticklabels(np.linspace(0, 82, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 7).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 320)
ax2.set_xlim(min(ADAT0)-5, 320)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate183.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18193
order0=dslist[7].sort_values("ADAT").index
order1=tplist[7].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[7].index)+1):
    if dslist[7]['ADAT'][i] < 2019000:
        val = dslist[7]['ADAT'][i] - 2018000
    else:
        val = dslist[7]['ADAT'][i] - 2019000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[7].index)+1):
    if tplist[7]['ADAT'][i] < 2019000:
        val = tplist[7]['ADAT'][i] - 2018000
    else:
        val = tplist[7]['ADAT'][i] - 2019000+365
    ADAT1.append(val)

val20_0 = len(dslist[7].index)*0.2
val50_0 = len(dslist[7].index)*0.5
val80_0 = len(dslist[7].index)*0.8
val20_1 = len(tplist[7].index)*0.2
val50_1 = len(tplist[7].index)*0.5
val80_1 = len(tplist[7].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(20*len(dslist[7].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(50*len(dslist[7].index)/100)],'ADAT']-2018000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(80*len(dslist[7].index)/100)],'ADAT']-2018000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(20*len(tplist[7].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(50*len(tplist[7].index)/100)],'ADAT']-2018000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(80*len(tplist[7].index)/100)],'ADAT']-2018000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 321, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 321, 5)))
ax.set_yticklabels(np.linspace(0, 90, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 84, 6).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 325)
ax2.set_xlim(min(ADAT0)-5, 325)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190222_sskt_eunjinwgen_adat_png/190222_CDF_SSKT_WgenEunjin_Anthesis_pdate193.png", bbox_inches='tight')
plt.show()


















