#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 23 17:01:21 2019

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
import json
import urllib.request


"""aasa
190123 check the data of new API

direct-sowing -> 5c481bbd9157060041e935e2
transplanting -> 5c4813b67c79d30033aa9161
"""

with urllib.request.urlopen('http://cropsim.service.listenfield.com/v1/simulations/5c4813b67c79d30033aa9161') as response:
    tp = response.read()
tp = json.loads(tp)

with urllib.request.urlopen('http://cropsim.service.listenfield.com/v1/simulations/5c481bbd9157060041e935e2') as response:
    ds = response.read()
ds = json.loads(ds)

tp_yield = []
ds_yield = []
for i in range(1, len(tp["result"])):
    tp_yield.append(tp["result"][i][10])
    ds_yield.append(ds["result"][i][10])

tp_yield = np.asarray(tp_yield, dtype=np.float32)
ds_yield = np.asarray(ds_yield, dtype=np.float32)

yield_val = np.concatenate((tp_yield.reshape(-1,1), ds_yield.reshape(-1,1)), axis=1)

y_df = pd.DataFrame(yield_val, index=np.arange(1, 101, 1), columns=["TP", "DS"])

DS_order = y_df.sort_values("DS").index
DS_df = pd.DataFrame(np.arange(1,101,1), index=DS_order, columns=["DS_ORDER"])

TP_order = y_df.sort_values("TP").index
TP_df = pd.DataFrame(np.arange(1,101,1), index=TP_order, columns=["TP_ORDER"])

y_df = pd.concat([y_df, DS_df, TP_df], axis=1, sort=True)



"""
190123 generate cumulative distribution graph
"""

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

yy1_0 = y_df[y_df["DS_ORDER"]==50]["DS"].values[0]*0.7
yy2_0 = y_df[y_df["DS_ORDER"]==50]["DS"].values[0]*0.2
Ind0 = np.abs(y_df["DS"].values - yy1_0).argmin()+1 
yy1_1 = y_df[y_df["TP_ORDER"]==50]["TP"].values[0]*0.7
yy2_1 = y_df[y_df["TP_ORDER"]==50]["TP"].values[0]*0.2
Ind1 = np.abs(y_df["TP"].values - yy1_1).argmin()+1 

ax.hist(y_df['DS'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([1000, 6000],[20, 20], color="black", label="20 percentile Yield="+repr(y_df[y_df["DS_ORDER"]==20]["DS"].values[0])+"kg/ha")
ax.plot([1000, 6000],[50, 50], color="blue", label="50 percentile Yield="+repr(y_df[y_df["DS_ORDER"]==50]["DS"].values[0])+"kg/ha")
ax.plot([1000, 6000],[80, 80], color="orange", label="80 percentile Yield="+repr(y_df[y_df["DS_ORDER"]==80]["DS"].values[0])+"kg/ha")
ax.plot([yy1_0, yy1_0],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(y_df.loc[Ind0,"DS_ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(y_df['TP'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([1000, 6000],[20, 20], color="black", label="20 percentile Yield="+repr(y_df[y_df["TP_ORDER"]==20]["TP"].values[0])+"kg/ha")
ax2.plot([1000, 6000],[50, 50], color="blue", label="50 percentile Yield="+repr(y_df[y_df["TP_ORDER"]==50]["TP"].values[0])+"kg/ha")
ax2.plot([1000, 6000],[80, 80], color="orange", label="80 percentile Yield="+repr(y_df[y_df["TP_ORDER"]==80]["TP"].values[0])+"kg/ha")
ax2.plot([yy1_1, yy1_1],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(y_df.loc[Ind1,"TP_ORDER"])+"%")
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
#plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Yield_TP_VS_DS.png", bbox_inches='tight')

plt.show()









