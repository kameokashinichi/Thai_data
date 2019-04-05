#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 28 12:10:17 2019

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
190128 check if the impact of weather data against yield is correct or not(Transplanting)

Place -> Roiet
ID -> 2019-01-27T15-48-03-880Zdebdb4858a2d9a2b
transplant_date -> 18194
icnd -> 700
icrt -> 0
icres -> 0
"""

record = []
with open(os.getcwd() + '/2019-01-27T15-48-03-880Zdebdb4858a2d9a2b/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
#record = np.asarray(record)
    
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    if len(rec) == 82:
        summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_dfT = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

val = sum_dfT.loc[:, ["HWAH","ADAT","MDAT"]].values.astype(np.int32)

sum_dfT = pd.DataFrame(val, index=np.arange(1,100), columns=["HWAH","ADAT","MDAT"])

min(sum_dfT["HWAH"])

#visualize the data into cumulative distribution.

order = sum_dfT.sort_values("HWAH").index
ord_df = pd.DataFrame(np.arange(1,100), index=order, columns=['ORDER'])
sum_ds = pd.concat([sum_dfT, ord_df], axis=1, sort=True)

val = sum_dfT['HWAH'].values

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

yy1 = sum_dfT.loc[order[50],'HWAH']*0.7
yy2 = sum_dfT.loc[order[50],'HWAH']*0.2
Ind = np.abs(val - 3000).argmin()+1 

ax.hist(val, bins=100, cumulative=True, color='red', histtype="barstacked")
ax.plot([2500, 3800],[20, 20], color="black", label="20 percentile Yield="+repr(sum_dfT.loc[order[20],'HWAH'])+"kg/ha")
ax.plot([2500, 3800],[50, 50], color="blue", label="50 percentile Yield="+repr(sum_dfT.loc[order[50],'HWAH'])+"kg/ha")
ax.plot([2500, 3800],[80, 80], color="orange", label="80 percentile Yield="+repr(sum_dfT.loc[order[80],'HWAH'])+"kg/ha")
ax.plot([3000, 3000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds.loc[Ind,"ORDER"])+"%")


plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Yield(Direct-sowing)", fontsize=18)
ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190108_Reiton_RIX_png/190111_CDF_Roiet_Yield_ds_pdate194.png", bbox_inches='tight')
plt.show()


"""
190128 check if the impact of weather data against yield is correct or not(Direct-sowing)

Place -> Roiet
ID -> 2019-01-28T06-33-55-868Zdec258396cb479de
planting_date -> 18174
icnd -> 700
icrt -> 0
icres -> 0
"""

record = []
with open(os.getcwd() + '/2019-01-28T06-33-55-868Zdec258396cb479de/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
#record = np.asarray(record)
    
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    if len(rec) == 82:
        summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df2T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

val = sum_df2T.loc[:, ["HWAH","ADAT","MDAT"]].values.astype(np.int32)

sum_df2T = pd.DataFrame(val, index=np.arange(1,100), columns=["HWAH","ADAT","MDAT"])


#visualize the data into cumulative distribution.

order = sum_df2T.sort_values("HWAH").index
ord_df = pd.DataFrame(np.arange(1,100), index=order, columns=['ORDER'])
sum_ds = pd.concat([sum_dfT, ord_df], axis=1, sort=True)

val = sum_df2T['HWAH'].values

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

yy1 = sum_dfT.loc[order[50],'HWAH']*0.7
yy2 = sum_dfT.loc[order[50],'HWAH']*0.2
Ind = np.abs(val - 3000).argmin()+1 

ax.hist(val, bins=100, cumulative=True, color='red', histtype="barstacked")
ax.plot([1000, 3800],[20, 20], color="black", label="20 percentile Yield="+repr(sum_df2T.loc[order[20],'HWAH'])+"kg/ha")
ax.plot([1000, 3800],[50, 50], color="blue", label="50 percentile Yield="+repr(sum_df2T.loc[order[50],'HWAH'])+"kg/ha")
ax.plot([1000, 3800],[80, 80], color="orange", label="80 percentile Yield="+repr(sum_df2T.loc[order[80],'HWAH'])+"kg/ha")
ax.plot([3000, 3000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds.loc[Ind,"ORDER"])+"%")


plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Yield(Transplanting)", fontsize=18)
ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190108_Reiton_RIX_png/190111_CDF_Roiet_Yield_ds_pdate194.png", bbox_inches='tight')
plt.show()


#compare both
order0 = sum_dfT.sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,100), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([sum_dfT, ord_df0], axis=1, sort=True)
order1 = sum_df2T.sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,100), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([sum_df2T, ord_df1], axis=1, sort=True)

val0 = sum_dfT['HWAH'].values
val1 = sum_df2T['HWAH'].values

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

yy1_0 = sum_dfT.loc[order0[50],'HWAH']*0.7
yy2_0 = sum_dfT.loc[order0[50],'HWAH']*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - 3000).argmin()+1 
yy1_1 = sum_df2T.loc[order1[50],'HWAH']*0.7
yy2_1 = sum_df2T.loc[order1[50],'HWAH']*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - 3000).argmin()+1 

ax.hist(sum_dfT['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([1000, 3800],[20, 20], color="black", label="20 percentile Yield="+repr(sum_dfT.loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([1000, 3800],[50, 50], color="blue", label="50 percentile Yield="+repr(sum_dfT.loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([1000, 3800],[80, 80], color="orange", label="80 percentile Yield="+repr(sum_dfT.loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([3000, 3000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(sum_df2T['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([1000, 3800],[20, 20], color="black", label="20 percentile Yield="+repr(sum_df2T.loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([1000, 3800],[50, 50], color="blue", label="50 percentile Yield="+repr(sum_df2T.loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([1000, 3800],[80, 80], color="orange", label="80 percentile Yield="+repr(sum_df2T.loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([3000, 3000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing)", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting)", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190128_CDF_Roiet_Yield_TP_VS_DS.png", bbox_inches='tight')

plt.show()














