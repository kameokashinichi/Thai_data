#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 14 04:04:07 2019

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


def getCropsimResult(sNo):

    url = "http://cropsim.service.listenfield.com/v1/simulations/"+sNo
    
    payload = ""
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "49e5a4ff-aea6-4d5f-8eb5-b0a0b298f28c"
        }
    
    response = requests.request("GET", url, data=payload, headers=headers)
    
    js = response.json()["result"]
    arr = np.asarray(js)
    print(arr.shape)
    df = pd.DataFrame(arr[1:, :], index=np.arange(1, 101), columns=arr[0, :])    
    df = df.iloc[:,6:11]
    return df

"""
190214_Transplant VS Direct-sowing in May, June and July in Reitong

Direct-sowing in 18143 -> "2019-01-10T05-38-16-196Z0dd6e68de7570f4c"
Transplanting in 18163 -> "2019-01-10T06-11-52-890Za539c53524cb906e"
Direct-sowing in 18123 -> "http://cropsim.service.listenfield.com/v1/simulations/5c646d7efe29b0003fff27ce"
Direct-sowing in 18133 -> "http://cropsim.service.listenfield.com/v1/simulations/5c646ec9b0a0e3004d78a6da"
Direct-sowing in 18143 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647ab7b0a0e3004d78a6e6"
Direct-sowing in 18153 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6475bcb0a0e3004d78a6dd"
Direct-sowing in 18163 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647573fe29b0003fff27cf"
Direct-sowing in 18173 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647638b0a0e3004d78a6de"
Direct-sowing in 18183 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6476a2b0a0e3004d78a6df"
Direct-sowing in 18193 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647700b0a0e3004d78a6e0"
Transplanting in 18193 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647777fe29b0003fff27d0"
Transplanting in 18203 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6477d6fe29b0003fff27d1"
Transplanting in 18213 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647834fe29b0003fff27d2"
Transplanting in 18183 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6478a1b0a0e3004d78a6e1"
Transplanting in 18173 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6478f8b0a0e3004d78a6e2"
Transplanting in 18163 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647958b0a0e3004d78a6e3"
Transplanting in 18153 -> "http://cropsim.service.listenfield.com/v1/simulations/5c6479d6b0a0e3004d78a6e4"
Transplanting in 18143 -> "http://cropsim.service.listenfield.com/v1/simulations/5c647a4fb0a0e3004d78a6e5"

the columns of each df
['planting_date (yyyy-mm-dd)', 'transplant_date (yyyy-mm-dd)',
       'anthesis_date (yyyy-mm-dd)', 'physiologic_maturity_dat (yyyy-mm-dd)',
       'HWAH'],

1. generate list for direct-sowing and transplanting simulation respectively.
2. compare the designated date of planting
"""

#direct-sowing list
dslist = []
ds_id = ["5c646d7efe29b0003fff27ce", "5c646ec9b0a0e3004d78a6da", 
         "5c647ab7b0a0e3004d78a6e6", "5c6475bcb0a0e3004d78a6dd", 
         "5c647573fe29b0003fff27cf", "5c647638b0a0e3004d78a6de",
         "5c6476a2b0a0e3004d78a6df", "5c647700b0a0e3004d78a6e0"]

for i in range(len(ds_id)):
    df = getCropsimResult(ds_id[i])
    dslist.append(df)

#transplanting list
tplist = []
tp_id = ["5c647a4fb0a0e3004d78a6e5", "5c6479d6b0a0e3004d78a6e4", 
         "5c647958b0a0e3004d78a6e3", "5c6478f8b0a0e3004d78a6e2", 
         "5c6478a1b0a0e3004d78a6e1", "5c647777fe29b0003fff27d0", 
         "5c6477d6fe29b0003fff27d1", "5c647834fe29b0003fff27d2"]

for i in range(len(tp_id)):
    df = getCropsimResult(tp_id[i])
    tplist.append(df)

#compare these two
order0 = dslist[0].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[0], ord_df0], axis=1, sort=True)
order1 = tplist[0].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[0], ord_df1], axis=1, sort=True)

val0 = dslist[0]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[0]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 5000

yy1_0 = float(dslist[0].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[0].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[0].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[0].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[0].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[0].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[0].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19123.png", bbox_inches='tight')

plt.show()


os.mkdir("190214_Reitong_cumulative")


#compare these two ~the middle of May~
order0 = dslist[1].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[1].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[1]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[1]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 5000

yy1_0 = float(dslist[1].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[1].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[1].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[1].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[1].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[1].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[1].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19133.png", bbox_inches='tight')

plt.show()


#compare these two ~the late May~
order0 = dslist[2].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[2].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[2]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[2]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 5000

yy1_0 = float(dslist[2].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[2].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[2].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[2].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[2].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[2].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[2].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in late May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19143.png", bbox_inches='tight')

plt.show()


#compare these two ~the early June~
order0 = dslist[3].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[3].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[3]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[3]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 4000

yy1_0 = float(dslist[3].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[3].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[3].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[3].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[3].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[3].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[3].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early June", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19153.png", bbox_inches='tight')

plt.show()

#compare these two ~the middle June~
order0 = dslist[4].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[4].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[4]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[4]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 4000

yy1_0 = float(dslist[4].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[4].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[4].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[4].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[4].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[4].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[4].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle June", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19163.png", bbox_inches='tight')

plt.show()

#compare these two ~the late June~
order0 = dslist[5].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[5].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[5]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[5]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[5].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[5].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[5].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[5].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[5].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[5].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[5].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in late June", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19173.png", bbox_inches='tight')

plt.show()


#compare these two ~the early July~
order0 = dslist[6].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[6].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[6]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[6]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2000

yy1_0 = float(dslist[6].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[6].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[6].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[6].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[6].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[6].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[6].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early July", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19183.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle July~
order0 = dslist[7].sort_values("harvest_amount (kg/ha)").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[7].sort_values("harvest_amount (kg/ha)").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[7]['harvest_amount (kg/ha)'].values.astype(np.float32)
val1 = tplist[7]['harvest_amount (kg/ha)'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2000

yy1_0 = float(dslist[7].loc[order0[50],'harvest_amount (kg/ha)'])*0.7
yy2_0 = float(dslist[7].loc[order0[50],'harvest_amount (kg/ha)'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[7].loc[order1[50],'harvest_amount (kg/ha)'])*0.7
yy2_1 = float(tplist[7].loc[order1[50],'harvest_amount (kg/ha)'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val0)],[20, 20], color="black", label="20 percentile Yield="+repr(dslist[7].loc[order0[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[50, 50], color="blue", label="50 percentile Yield="+repr(dslist[7].loc[order0[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([min(val0), max(val0)],[80, 80], color="orange", label="80 percentile Yield="+repr(dslist[7].loc[order0[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[Ind0,"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val1), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[20],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[50],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([min(val1), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[80],'harvest_amount (kg/ha)'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[Ind1,"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle July", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190214_Reitong_cumulative/190214_CDF_Reiton_Yield_TP_VS_DS_19193.png", bbox_inches='tight')

plt.show()



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
    with open(os.getcwd() + '/190218_cumdata/'+ds_id[i]+'/Summary.OUT', 'r') as f:
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
    df = pd.DataFrame(val, index=summary[:, 0], columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    dslist.append(df)


#generate list which consists of the dataframe of Transplanting result
tplist = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190218_cumdata/'+tp_id[i]+'/Summary.OUT', 'r') as f:
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
    df = pd.DataFrame(val, index=summary[:, 0], columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)


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
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190218_CDF_Reiton_Yield_TP_VS_DS_18123.png", bbox_inches='tight')

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
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in middle May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190218_CDF_Reiton_Yield_TP_VS_DS_18133.png", bbox_inches='tight')

plt.show()


#compare these two ~the late May~
order0 = dslist[2].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[2].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

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
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in late May", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190218_CDF_Reiton_Yield_TP_VS_DS_18143.png", bbox_inches='tight')

plt.show()


#compare these two ~the early June~
order0 = dslist[3].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[3].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

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
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[20, 20], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[50, 50], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[80, 80], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram of Yield(transplanting) in early June", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190214_Reitong_cumulative/190219_CDF_Reiton_Yield_TP_VS_DS_18153.png", bbox_inches='tight')

plt.show()




