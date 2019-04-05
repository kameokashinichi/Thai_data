#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 21 09:27:55 2019

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



"""
190218 cumulative function of Direct-sowing VS Transplanting

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

ds_id = ["2019-02-18T06-58-44-229Zf0de45ee989c4be2", "2019-02-18T07-02-46-888Z1b134b4617d1ad9a",
          "2019-01-10T05-38-16-196Z0dd6e68de7570f4c", "2019-02-18T07-06-42-815Z92560c6b338928d1",
          "2019-02-18T07-10-47-438Z804a5ab3d565389f", "2019-02-18T07-13-58-272Z5f81b7cb8fac5e2c",
          "2019-02-18T07-17-40-806Z59ebf8c1d7283ce9", "2019-02-18T07-20-37-052Z97382381cc75e973"]

tp_id = ["2019-02-18T07-44-41-332Z92db5dff9619d2cb", "2019-02-18T07-41-56-188Z34aeb7eb0fae960d",
          "2019-01-10T06-11-52-890Za539c53524cb906e", "2019-02-18T07-39-16-877Z6c06de3ff36e7614",
          "2019-02-18T07-36-17-366Z752842139ba27c6c", "2019-02-18T07-27-01-220Z15022c8724634e9a",
          "2019-02-18T07-29-56-899Z6ad48cbfaea9e270", "2019-02-18T07-33-01-385Z8ae90b6dc1e2b442"]


#generate list which consists of the dataframe of Direct-sowing result
dslist = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190218_cumdata_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    for i in range(4, len(record)):
        rec = record[i].split()
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
    with open(os.getcwd() + '/190218_cumdata_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
            
    summary = []
    for i in range(4, len(record)):
        rec = record[i].split()
        summary.append(rec)
    
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)

#make directory
os.mkdir("190221_yield_cumulative_reiton_wgen")

#compare these two ~tpdate == 18123~
order0 = dslist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[0], ord_df0], axis=1, sort=True)
order1 = tplist[0].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[0], ord_df1], axis=1, sort=True)

val0 = dslist[0]['HWAH'].values.astype(np.float32)
val1 = tplist[0]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[0].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[0].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[0].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[0].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[0].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[0].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[0].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190218_CDF_Reiton_Yield_TP_VS_DS_18123_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18133~
order0 = dslist[1].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[1].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[1]['HWAH'].values.astype(np.float32)
val1 = tplist[1]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[1].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[1].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[1].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[1].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[1].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[1].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[1].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190218_CDF_Reiton_Yield_TP_VS_DS_18133_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the late May~
order0 = dslist[2].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[2], ord_df0], axis=1, sort=True)
order1 = tplist[2].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[2], ord_df1], axis=1, sort=True)

val0 = dslist[2]['HWAH'].values.astype(np.float32)
val1 = tplist[2]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[2].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[2].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[2].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[2].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[2].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[2].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[2].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190218_CDF_Reiton_Yield_TP_VS_DS_18143_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the early June~
order0 = dslist[3].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[3], ord_df0], axis=1, sort=True)
order1 = tplist[3].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[3], ord_df1], axis=1, sort=True)

val0 = dslist[3]['HWAH'].values.astype(np.float32)
val1 = tplist[3]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[3].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[3].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[3].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[3].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[3].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[3].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[3].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190219_CDF_Reiton_Yield_TP_VS_DS_18153_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle June~
order0 = dslist[4].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[4], ord_df0], axis=1, sort=True)
order1 = tplist[4].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[4], ord_df1], axis=1, sort=True)

val0 = dslist[4]['HWAH'].values.astype(np.float32)
val1 = tplist[4]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[4].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[4].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[4].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[4].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[4].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[4].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[4].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190219_CDF_Reiton_Yield_TP_VS_DS_18163_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the late June~
order0 = dslist[5].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[5], ord_df0], axis=1, sort=True)
order1 = tplist[5].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[5], ord_df1], axis=1, sort=True)

val0 = dslist[5]['HWAH'].values.astype(np.float32)
val1 = tplist[5]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[5].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[5].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[5].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[5].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[5].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[5].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[5].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190219_CDF_Reiton_Yield_TP_VS_DS_18173_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the early July~
order0 = dslist[6].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[6], ord_df0], axis=1, sort=True)
order1 = tplist[6].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[6], ord_df1], axis=1, sort=True)

val0 = dslist[6]['HWAH'].values.astype(np.float32)
val1 = tplist[6]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[6].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[6].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[6].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[6].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[6].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[6].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[6].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190219_CDF_Reiton_Yield_TP_VS_DS_18183_wgen.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle July~
order0 = dslist[7].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[7], ord_df0], axis=1, sort=True)
order1 = tplist[7].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[7], ord_df1], axis=1, sort=True)

val0 = dslist[7]['HWAH'].values.astype(np.float32)
val1 = tplist[7]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2500

yy1_0 = float(dslist[7].loc[order0[50],'HWAH'])*0.7
yy2_0 = float(dslist[7].loc[order0[50],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[7].loc[order1[50],'HWAH'])*0.7
yy2_1 = float(tplist[7].loc[order1[50],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[7].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[7].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[7].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_yield_cumulative_reiton_wgen/190219_CDF_Reiton_Yield_TP_VS_DS_18193_wgen.png", bbox_inches='tight')

plt.show()


"""
#MATURITY DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190221_mdat_cumulative_reiton_wgen_png")

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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-7, max(mdat0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-7, max(mdat0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 90, 7))
#ax2.set_yticklabels(np.linspace(0, 90, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate123.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-5, max(mdat0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-5, max(mdat0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 90, 7))
#ax2.set_yticklabels(np.linspace(0, 90, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate133.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-7, max(mdat0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-7, max(mdat0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate143.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-4, max(mdat0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-4, max(mdat0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate153.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-6, max(mdat0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-6, max(mdat0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, max(mdat0)+5)
ax2.set_xlim(min(mdat0)-5, max(mdat0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate163.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-5, 330, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-5, 330, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, 330)
ax2.set_xlim(min(mdat0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate173.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-6, 330, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-6, 330, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, 330)
ax2.set_xlim(min(mdat0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate183.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(mdat0)-8, 340, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(mdat0)-8, 340, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(mdat0)-5, 340)
ax2.set_xlim(min(mdat0)-5, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_mdat_cumulative_reiton_wgen_png/190221_CDF_SSKT_Wgen_Maturity_pdate193.png", bbox_inches='tight')
plt.show()


"""
#ANTHESIS DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190221_adat_cumulative_reiton_wgen_png")

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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 90, 7))
#ax2.set_yticklabels(np.linspace(0, 90, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate123.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 93, 7))
#ax2.set_yticklabels(np.linspace(0, 93, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate133.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 93, 7))
#ax2.set_yticklabels(np.linspace(0, 93, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0))
ax2.set_xlim(min(ADAT0)-5, max(ADAT0))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate143.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, max(ADAT0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+10)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate153.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate163.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 310, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 310, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, 310)
ax2.set_xlim(min(ADAT0)-5, 310)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate173.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, 315, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, 315, 5)))
#ax.set_yticklabels(np.linspace(0, 96, 7))
#ax2.set_yticklabels(np.linspace(0, 96, 7))
ax.set_xlim(min(ADAT0)-5, 310)
ax2.set_xlim(min(ADAT0)-5, 310)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate183.png", bbox_inches='tight')
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
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-4, 321, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-4, 321, 5)))
#ax.set_yticklabels(np.linspace(0, 87.5, 6))
#ax2.set_yticklabels(np.linspace(0, 87.5, 6))
ax.set_xlim(min(ADAT0)-5, 320)
ax2.set_xlim(min(ADAT0)-5, 320)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190221_adat_cumulative_reiton_wgen_png/190220_CDF_SSKT_Wgen_Anthesis_pdate193.png", bbox_inches='tight')
plt.show()






















