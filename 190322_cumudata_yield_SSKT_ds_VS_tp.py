#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 22 15:42:31 2019

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
from urllib import request
import zipfile
import shutil


"""
190322 convert SSKT_WTH/SSKT00xx.WTH file into COMM00xx.WTDE and 00xx1801.WTH respectively

1. Make directory for weather file
2. copy, then rename the WTH into 00xx.WTH
3. use WTH2Dataframe2, then dataframe2wtd to generate COMM00xx.WTDE

['SSKT0001.WTH', 00011801
 'SSKT0101.WTH', 00021801
 'SSKT0201.WTH', 00031801
 'SSKT0301.WTH',
 'SSKT0401.WTH',
 'SSKT0501.WTH',
 'SSKT0601.WTH',
 'SSKT0701.WTH',
 'SSKT0801.WTH',
 'SSKT0901.WTH',
 'SSKT1001.WTH',
 'SSKT1101.WTH',
 'SSKT1201.WTH',
 'SSKT1301.WTH',
 'SSKT1401.WTH',
 'SSKT1501.WTH',
 'SSKT1601.WTH',
 'SSKT1701.WTH',
 'SSKT1801.WTH',
 'SSKT8601.WTH',
 'SSKT8701.WTH',
 'SSKT8801.WTH',
 'SSKT8901.WTH',
 'SSKT9001.WTH',
 'SSKT9101.WTH',
 'SSKT9201.WTH',
 'SSKT9301.WTH',
 'SSKT9401.WTH',
 'SSKT9501.WTH',
 'SSKT9601.WTH',
 'SSKT9701.WTH',
 'SSKT9801.WTH',
 'SSKT9901.WTH'  00331801]
"""

#1 make directory
os.mkdir("sskt_past_weather")

#2copy, then rename
sskt = list(filter(lambda x: re.search(".WTH", x), os.listdir("SSKT_WTH")))
sskt.sort()

for i in range(len(sskt)):
    #print("sskt_past_weather/"+repr(i+1).zfill(4)+"1801.WTH")
    shutil.copy2(src="SSKT_WTH/"+sskt[i], dst="sskt_past_weather")
    os.rename(src="sskt_past_weather/"+sskt[i], dst="sskt_past_weather/"+repr(i+1).zfill(4)+"1801.WTH")

#3. use WTH2Dataframe2, then dataframe2wtd to generate COMM00xx.WTDE
for i in range(len(sskt)):
    #print("sskt_past_weather/COMM"+repr(i+1).zfill(4))
    df = WTH2Dataframe2("SSKT_WTH/"+sskt[i])
    day = pd.DataFrame(np.arange(1, len(df.index)+1), index=df.index, columns=["DAY"])
    year = pd.DataFrame(np.repeat(2018, len(df.index)), index=df.index, columns=["YEAR"])
    df = pd.concat([df, day, year], axis=1)
    wtd = dataframe2wtd(df, "sskt_past_weather/COMM"+repr(i+1).zfill(4), add_tave=True, to_slice=False, to_check=True, out_extension = ".WTDE")


"""
change the year data in WTH and WTDE
"""
#1 WTH
wth = list(filter(lambda x: re.search(".WTH", x), os.listdir("sskt_past_weather")))

for i in range(len(wth)):
    n = 0
    lis = []
    with open("sskt_past_weather/"+wth[i], "r") as f:
        for row in f:
            if re.search("\d{2}", row[:2]):
                lis.append("18"+row[2:])
            else:
                lis.append(row)
            n = n+1
    
    with open("sskt_past_weather/"+wth[i], "w") as f:
        for j in range(len(lis)):
            f.write(lis[j])


"""
Run dssat via API

1. generate payload
2. run via API, then download results

weather_file -> "http://dev.listenfield.com/cropsim/uploads/2019-03-22T07-58-03-780Zbb758073bdfd78d7/sskt_past_weather.zip"
directory name -> "190322_sskt_cumudata_past_30years"
"""

#run dssat API
os.mkdir("190322_sskt_cumudata_past_30years")

ds_date = ["2018-05-03", "2018-05-13", "2018-05-23", "2018-06-02", "2018-06-12", 
           "2018-06-22", "2018-07-02", "2018-07-12"]
tp_date = ["2018-05-23", "2018-06-02", "2018-06-12", 
           "2018-06-22", "2018-07-02", "2018-07-12", "2018-07-22", "2018-08-01"]


for i in range(0, 2):
    if i == 0:
        for j in range(len(ds_date)):
            jinfo = generateDssatSSKT(ds_date[j], "http://dev.listenfield.com/cropsim/uploads/2019-03-22T07-58-03-780Zbb758073bdfd78d7/sskt_past_weather.zip",  pmethod="S")
            getDssatData(jinfo, "190322_sskt_cumudata_past_30years")
    else:
        for j in range(len(tp_date)):
            jinfo = generateDssatSSKT(tp_date[j], "http://dev.listenfield.com/cropsim/uploads/2019-03-22T07-58-03-780Zbb758073bdfd78d7/sskt_past_weather.zip",  pmethod="T")
            getDssatData(jinfo, "190322_sskt_cumudata_past_30years")        


"""
generate graph

"""
ids = list(filter(lambda x: re.search("^2019", x), os.listdir("190322_sskt_cumudata_past_30years")))
ids.sort()


"""
Direct-sowing in 18123 -> '2019-03-22T07-28-00-137Z9a2b081b068f929b'
Direct-sowing in 18133 -> '2019-03-22T07-26-12-054Z299a8ff2cf86c74a'
Direct-sowing in 18143 -> '2019-03-22T07-26-13-484Z562340668b56d0cb'
Direct-sowing in 18153 -> '2019-03-22T07-26-15-027Z31103f1e6cd0abd8'
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

ds_id = ids[:8]
tp_id = ids[8:]

#generate list which consists of the dataframe of Direct-sowing result
dslist = []
dserr = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + "/190322_sskt_cumudata_past_30years/"+ds_id[i]+'/Summary.OUT', 'r') as f:
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
    with open(os.getcwd() + "/190322_sskt_cumudata_past_30years/"+tp_id[i]+'/Summary.OUT', 'r') as f:
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



os.mkdir("190322_sskt_past_30years_yield_png")

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -past 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
ax.set_xlim(2500, 5500)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index)+5)
#ax2.set_ylim(0, len(sum_ds1.index)+5)
plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18123_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 5500)
plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18133_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 5500)
plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18143_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2000, 5500)
#plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18153_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, 82, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 4800)
#plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18163_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, 82, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 4900)
#plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18173_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, 83, 5).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, 84, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4500)
#plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18183_WGEN_PAST30.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,35], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("The number of samples", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -PAST 30years-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("The number of samples", fontsize=16)
#ax.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
#ax2.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4100)
#plt.savefig("190322_sskt_past_30years_yield_png/190322_CDF_Reiton_Yield_TP_VS_DS_18193_WGEN_PAST30.png", bbox_inches='tight')

plt.show()






"""
lis = list(filter(lambda x: re.search("COMM", x), os.listdir("./")))

os.chdir("Bias_corrected_WTDE")
for i in range(len(lis)):
    os.rename(lis[i], "COMM"+repr(i+1).zfill(4)+".WTDE")

#2. generate 100 "00xx1801.WTH" file by using "gencli.a" and "genWTH.a" via subprocess module
#3. store these data into one directory
for i in range(1, 101):
    #os.chdir("/Users/kameokashinichi/Documents/postdoc/crop_util")
    
    subprocess.call(["./genCLI.a", "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/COMM"+repr(i).zfill(4)+".WTDE",
                     repr(i).zfill(4), "15.000", "104.050", "4"])
    subprocess.call(["./genWTH.a", repr(i).zfill(4)+".CLI", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/COMM"+repr(i).zfill(4)+".WTDE"])
    subprocess.call(["mv", repr(i).zfill(4)+"1801.WTH", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/"])
    subprocess.call(["mv", repr(i).zfill(4)+".CLI", 
                     "./eunjin_cli/"])

"""    
"""
190223 simulate the date

weather_file -> "http://dev.listenfield.com:3232/cropsim/uploads/2019-02-23T03-03-44-228Zf03e556072c02591/Bias_corrected_WTDE.zip"
"""    
    
def generateDssatSSKT(pdate, w_file,  pmethod="S"):
    """
    pdate  : str (ex. 'yyyy-mm-dd')
        the transplanting date for simulation
    w_file : str
        the link of the weather scenario 
    pmethod: str
        "S"->Direct-sowing, "T"->Transplanting
        
    download result csv file
    """
    url = "http://dev.listenfield.com:3232/cropsim/v1.1/simulations"
    
    payload = {
  "planting_date": pdate,
  "crop_ident_ICASA": "RIC",
  "cultivar_name": "KDML105",
  "model": "dssat",
  "weather_file": w_file,
  "wait": "true",
  "model_params": 
  {
    "id_soil": "JP_NRPH10F",
    "initial_conditions":[
      {
        "ic_num": "1",
        "pcr": "SB",
        "icdat": repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),   
        "icrt": "100",
        "icnd": "100",
        "icrn": "1",
        "icre": "1",
        "icwd": "-99",
        "icres": "100",   
        "icren": "0.8",
        "icrep": "0",
        "icrip": "100",
        "icrid": "15",
        "icname": "-99",
        "base_layers": [
          { "icbl": "5", "sh2o": "0.05", "snh4": "2.50", "sno3": "7.14" },
          { "icbl": "15", "sh2o": "0.07", "snh4": "2.57", "sno3": "4.66" },
          { "icbl": "30", "sh2o": "0.05", "snh4": "0.04", "sno3": "3.88" },
          { "icbl": "42", "sh2o": "0.04", "snh4": "0.07", "sno3": "3.71" },
          { "icbl": "55", "sh2o": "0.04", "snh4": "0.03", "sno3": "1.37" },
          { "icbl": "67", "sh2o": "0.05", "snh4": "0.01", "sno3": "0.98" },
          { "icbl": "80", "sh2o": "0.07", "snh4": "0.01", "sno3": "1.06" },
          { "icbl": "100", "sh2o": "0.05", "snh4": "0.01", "sno3": "1.23" }
        ]
      }
    ],
        "planting_details":[
    	{
		"p_num":"1",
		"pdate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])),   
		"edate":"-99",
		"ppop":"6.2",
		"ppoe":"6.2",
		"plme":pmethod,   
		"plds":"R",
		"plrs":"80",
		"plrd":"0",
		"pldp":"5",
		"plwt":"-99",
		"page":"20",
		"penv":"25",
		"plph":"-99",
		"sprl":"0",
		"plname":"-99"
	  }
	],
    "irrigations":[
    {
            "ir_num": "1",
            "efir": "-99",
            "idep": "-99",
            "ithr": "-99",
            "iept": "-99",
            "ioff": "-99",
            "iame": "-99",
            "iamt": "1",
            "irname": "NONE",
            "operations": [
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR010","irval":"0"},
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR008","irval":"2"},
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR009","irval":"150"}
	    	]
		}
	],
    "residues":[
		{
		"r_num":"1",
		"rdate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),
		"rcod":"RE999",
        "ramt": "600",
        "resn": "3.5",
        "resp": "0.5",
        "resk": "-99",
        "rinp": "-99",
        "rdep": "15",
        "rmet": "-99",
        "rename": "-99"
		}
      ],
    "simulation_controls":[
		{
          "n_num": "1",
          "general": "GE",
          "nyers": "1",
          "nreps": "1",
          "start": "S",
          "sdate": repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),  
          "rseed": "2150",
          "sname": "UNKNOWN",
          "smodel": "",
          "options": "OP",
          "water": "Y",
          "nitro": "Y",
          "symbi": "N",
          "phosp": "N",
          "potas": "N",
          "dises": "N",
          "chem": "N",
          "till": "N",
          "co2": "M",
          "methods": "ME",
          "wther": "M",
          "incon": "M",
          "light": "E",
          "evapo": "R",
          "infil": "S",
          "photo": "C",
          "hydro": "R",
          "nswit": "1",
          "mesom": "P",
          "mesev": "S",
          "mesol": "2",
          "management": "MA",
          "plant": "R",
          "irrig": "R",
          "ferti": "R",
          "resid": "R",
          "harvs": "M",
          "outputs": "OU",
          "fname": "N",
          "ovvew": "Y",
          "sumry": "Y",
          "fropt": "1",
          "grout": "Y",
          "caout": "N",
          "waout": "Y",
          "niout": "Y",
          "miout": "N",
          "diout": "N",
          "vbose": "D",
          "chout": "N",
          "opout": "N",
          "planting": "PL",
          "pfrst": "85028",
          "plast": "85042",
          "ph2ol": "40",
          "ph2ou": "100",
          "ph2od": "30",
          "pstmx": "40",
          "pstmn": "10",
          "irrigation": "IR",
          "imdep": "30",
          "ithrl": "50",
          "ithru": "100",
          "iroff": "IB001",
          "imeth": "IB001",
          "iramt": "10",
          "ireff": "1",
          "nitrogen": "NI",
          "nmdep": "30",
          "nmthr": "50",
          "namnt": "25",
          "ncode": "IB001",
          "naoff": "IB001",
          "residues": "RE",
          "ripcn": "100",
          "rtime": "1",
          "ridep": "20",
          "harvest": "HA",
          "hfrst": "0",
          "hlast": "86035",
          "hpcnp": "100",
          "hpcnr": "0"	
		}
    ]      
  }
}   
        
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "a65dd381-a65c-43d7-80f9-a183d50bd3f4"
        }
    
    payload = json.dumps(payload)
    
    response = requests.request("POST", url, data=payload, headers=headers)

    jinfo = json.loads(response.text)
    #csvlink = jinfo['csv_output']
    
    #print(type(csvlink))
    #request.urlretrieve(csvlink, folder + jinfo["id"] + '.csv')
    return jinfo


def getDssatData(jinfo, folder):
    """
    jinfo : dict
        the json file from Dssat API
    folder: str
        the name of the folder which stores data of the result
    """
    path = "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/"
    
    os.mkdir(path+folder+"/"+jinfo["id"])
    print(jinfo["id"])
    
    outputs = re.sub(":3232", "", jinfo['output_directory'])
    
    request.urlretrieve(outputs+"/Summary.OUT", path+folder+"/"+jinfo["id"]+"/"+"/Summary.OUT")
    request.urlretrieve(outputs+"/JPRI0001.RIX", path+folder+"/"+jinfo["id"]+"/"+"/JPRI0001.RIX")    
    request.urlretrieve(outputs+"/PlantGro.OUT", path+folder+"/"+jinfo["id"]+"/"+"/PlantGro.OUT")    
    request.urlretrieve(outputs+"/PlantN.OUT", path+folder+"/"+jinfo["id"]+"/"+"/PlantN.OUT")    
    request.urlretrieve(outputs+"/SoilNi.OUT", path+folder+"/"+jinfo["id"]+"/"+"/SoilNi.OUT")
    request.urlretrieve(outputs+"/SoilWat.OUT", path+folder+"/"+jinfo["id"]+"/"+"/SoilWat.OUT")
    
































    