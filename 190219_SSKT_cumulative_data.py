#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:16:11 2019

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
import subprocess
import json

"""
190211 generate weather file of SSKT

1. generate folder of the weather file.
2. devide WTD file into single year, then rename like "COMM00xx.WTDE"
3. copy the WTH file, then rename like 00xx1801.WTH
"""

#1 
os.mkdir("weather_file_SSKT")

#2
a = 1
for i in range(1986, 2018):
    WTD = []
    with open(os.getcwd() + '/SSKT.WTD' , 'r') as f:
        #print(type(f))
        n = 0
        for row in f:
            if row[:4] == repr(i):
                #print(row[:4])
                WTD.append("2018"+row[4:].strip())
                n = n+1
            elif n == 0:
                WTD.append(row.strip())
                n = n+1

    with open(os.getcwd()+"/weather_file_SSKT/COMM"+repr(a).zfill(4)+'.WTDE', 'w') as f:
        for row in WTD:
            f.write(row+"\n")
    a = a+1

#3
b = 1
for i in range(1986, 2018):
    WTH = []
    with open(os.getcwd() + '/SSKT_WTH/SSKT'+repr(i)[2:]+"01.WTH" , 'r') as f:
        for row in f:
            if re.search("^"+repr(i)[2:], row):
                r = "18"+row[2:]
                WTH.append(r)
            else:
                WTH.append(row)
                
    with open(os.getcwd()+"/weather_file_SSKT/"+repr(b).zfill(4)+'1801.WTH', 'w') as f:
        for row in WTH:
            f.write(row)
    b = b+1



"""
#confirmation code
WTD = []
with open(os.getcwd() + '/SSKT.WTD' , 'r') as f:
#print(type(f))
    n=0
    for row in f:
        if row[:4] == repr(1986):
            print("2018"+row[4:8])
            #WTD.append(row.strip())
            n = n+1
        elif n == 0:
            print(row[:8])
            n = n+1

with open('list.txt', 'w') as f:
    for row in WTD:
        f.write(row+"\n")
"""

"""
190219 compare tp VS ds

Direct-sowing in 18123 -> "2019-02-19T05-57-44-517Z1f203097e207a05d"
Direct-sowing in 18133 -> "2019-02-19T05-55-00-382Z60c8d147aa9ee679"
Direct-sowing in 18143 -> "2019-02-19T05-51-35-428Zb294d70780f26f35"
Direct-sowing in 18153 -> "2019-02-19T06-05-29-444Z7722c51ce8bd13d4"
Direct-sowing in 18163 -> "2019-02-19T06-09-06-705Z2c375fa33bbbe970"
Direct-sowing in 18173 -> "2019-02-19T06-11-27-477Z522b855f875f8d01"
Direct-sowing in 18183 -> "2019-02-19T06-13-41-240Z05d5aeecabdbf2a4"
Direct-sowing in 18193 -> "2019-02-19T06-16-13-925Z1833fce8c3eddaf0"
Transplanting in 18193 -> "2019-02-19T06-18-16-023Zc981cee5d9f8f224"
Transplanting in 18203 -> "2019-02-19T06-21-08-026Za144f5561f7ec74d"
Transplanting in 18213 -> "2019-02-19T06-23-57-285Zd503844c3c4c6e96"
Transplanting in 18183 -> "2019-02-19T06-27-11-991Ze46d5e31d74764aa"
Transplanting in 18173 -> "2019-02-19T06-30-02-137Z2bca3a0aae1a77aa"
Transplanting in 18163 -> "2019-02-19T06-32-14-870Zf74e607cbde8472d"
Transplanting in 18153 -> "2019-02-19T06-34-04-148Zd9d611fd576fb7b6"
Transplanting in 18143 -> "2019-02-19T06-36-03-391Zadd066ae307cda73"
"""

ds_id = ["2019-02-19T05-57-44-517Z1f203097e207a05d", "2019-02-19T05-55-00-382Z60c8d147aa9ee679",
          "2019-02-19T05-51-35-428Zb294d70780f26f35", "2019-02-19T06-05-29-444Z7722c51ce8bd13d4",
          "2019-02-19T06-09-06-705Z2c375fa33bbbe970", "2019-02-19T06-11-27-477Z522b855f875f8d01",
          "2019-02-19T06-13-41-240Z05d5aeecabdbf2a4", "2019-02-19T06-16-13-925Z1833fce8c3eddaf0"]

tp_id = ["2019-02-19T06-36-03-391Zadd066ae307cda73", "2019-02-19T06-34-04-148Zd9d611fd576fb7b6",
          "2019-02-19T06-32-14-870Zf74e607cbde8472d", "2019-02-19T06-30-02-137Z2bca3a0aae1a77aa",
          "2019-02-19T06-27-11-991Ze46d5e31d74764aa", "2019-02-19T06-18-16-023Zc981cee5d9f8f224",
          "2019-02-19T06-21-08-026Za144f5561f7ec74d", "2019-02-19T06-23-57-285Zd503844c3c4c6e96"]


#generate list which consists of the dataframe of Direct-sowing result
dslist = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190219_SSKT_actual_dssat/'+ds_id[i]+'/Summary.OUT', 'r') as f:
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
    
    #print(np.shape(sum_df5T))
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    dslist.append(df)


#generate list which consists of the dataframe of Transplanting result
tplist = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190219_SSKT_actual_dssat/'+tp_id[i]+'/Summary.OUT', 'r') as f:
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


#compare these two ~tpdate == 18123~
order0 = dslist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[0], ord_df0], axis=1, sort=True)
order1 = tplist[0].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[0], ord_df1], axis=1, sort=True)

val0 = sum_ds0['HWAH'].values.astype(np.float32)
val1 = sum_ds1['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[0].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[0].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early May-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 90, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18123.png", bbox_inches='tight')

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

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[1].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[1].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle May-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 90, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18133.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18143~
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

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[2].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[2].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in late May-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 90, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18143.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18153~
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

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[3].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[3].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early June-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 90, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18153.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18163~
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

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[4].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[4].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index)))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index)))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle June-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 96, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18163.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18173~
order0 = dslist[5].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[5], ord_df0], axis=1, sort=True)
order1 = tplist[5].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[5], ord_df1], axis=1, sort=True)

val0 = sum_ds0['HWAH'].values.astype(np.float32)
val1 = sum_ds1['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[5].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[5].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index)))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index)))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in late June-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 96, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18173.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18183~
order0 = dslist[6].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[6], ord_df0], axis=1, sort=True)
order1 = tplist[6].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[6], ord_df1], axis=1, sort=True)

val0 = sum_ds0['HWAH'].values.astype(np.float32)
val1 = sum_ds1['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2500

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[6].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[6].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index)))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index)))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early July-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 96, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18183.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18193~
order0 = dslist[7].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[7], ord_df0], axis=1, sort=True)
order1 = tplist[7].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[7], ord_df1], axis=1, sort=True)

val0 = sum_ds0['HWAH'].values.astype(np.float32)
val1 = sum_ds1['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2500

val20_0 = len(sum_ds0.index)*0.2
val50_0 = len(sum_ds0.index)*0.5
val80_0 = len(sum_ds0.index)*0.8
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 

val20_1 = len(sum_ds1.index)*0.2
val50_1 = len(sum_ds1.index)*0.5
val80_1 = len(sum_ds1.index)*0.8
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[val20_0, val20_0], color="black", label="20 percentile Yield="+repr(dslist[7].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val50_0, val50_0], color="blue", label="50 percentile Yield="+repr(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[val80_0, val80_0], color="orange", label="80 percentile Yield="+repr(dslist[7].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,len(sum_ds0.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]*100/len(sum_ds0.index)))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[val20_1, val20_1], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val50_1, val50_1], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[val80_1, val80_1], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,len(sum_ds1.index)], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]*100/len(sum_ds1.index)))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July-Actual-", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle July-Actual-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_yticklabels(np.linspace(0, 96, 7))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190219_CDF_SSKT_Actual_Yield_TP_VS_DS_18193.png", bbox_inches='tight')

plt.show()




"""
#MATURITY DATE, direct-sowing pattern -Actual-
"""
os.mkdir("190220_mdat_cumulative_SSKT_png")

order0=dslist[0].sort_values("MDAT").index
order1=tplist[0].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(len(dslist[0].index)):
    if dslist[0]['MDAT'][i] < 2019000:
        val = dslist[0]['MDAT'][i] - 2018000
    else:
        val = dslist[0]['MDAT'][i] - 2019000+365
    mdat0.append(val)

mdat1 = []
for i in range(len(tplist[0].index)):
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
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-10, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-10, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_yticklabels(np.linspace(0, 90, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate123.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-18, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-18, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_yticklabels(np.linspace(0, 90, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate133.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-15, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-15, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate143.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-20, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-20, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate153.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-14, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-14, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate163.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-19, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-19, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate173.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-21, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-21, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate183.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Actual-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-14, max(mdat0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-14, max(mdat0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
#ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
#ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_mdat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Maturity_pdate193.png", bbox_inches='tight')
plt.show()



"""
#ANTHESIS DATE, direct-sowing pattern -Actual-
"""
os.mkdir("190220_adat_cumulative_SSKT_png")

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
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Actual-", fontsize=18)
ax2.set_xlabel("The anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 90, 7))
ax2.set_yticklabels(np.linspace(0, 90, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate123.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 93, 7))
ax2.set_yticklabels(np.linspace(0, 93, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate133.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 93, 7))
ax2.set_yticklabels(np.linspace(0, 93, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate143.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-13, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-13, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate153.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate163.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 5)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate173.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, max(ADAT0)+10, 5)))
ax.set_yticklabels(np.linspace(0, 96, 7))
ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate183.png", bbox_inches='tight')
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
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Actual-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 87.5, 6))
ax2.set_yticklabels(np.linspace(0, 87.5, 6))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190220_adat_cumulative_SSKT_png/190220_CDF_SSKT_Actual_Anthesis_pdate193.png", bbox_inches='tight')
plt.show()










