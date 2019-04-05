#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 12 10:20:48 2019

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
from sklearn import linear_model
from matplotlib.patches import Polygon

"""
190112 The impact of El nino and La nina to yield (SSKT9605) 
"""
#read SSKT9605.OSU
record = []
with open('SSKT9605/SSKT9605.OSU', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(3, len(record)):
    nitro.append(record[i].split())
    
#nitro[0] = nitro[0][1:]
nitro = np.asarray(nitro)
nitro = nitro[:, 10:]
nitro = np.delete(nitro, 1, axis=1)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

sum_df_s = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

num = np.arange(0, 120, 4)
sum_df_s = sum_df_s.iloc[num]  #delete fallow index

sum_df_s["HWAH"]


#read SSKT9603.OSU
record = []
with open('SSKT9603/SSKT9603.OSU', "r") as f:
    for row in f:
        record.append(row.strip()) #strip removes \n code
        
nitro = []
for i in range(3, len(record)):
    nitro.append(record[i].split())
    
#nitro[0] = nitro[0][1:]
nitro = np.asarray(nitro)
nitro = nitro[:, 10:]
nitro = np.delete(nitro, 1, axis=1)
nitro2 = np.asarray(nitro[1:, 1:], dtype=np.float64)

sum_df_4 = pd.DataFrame(nitro2, index=nitro[1:, 0], columns=nitro[0, 1:])

num = np.arange(0, 120, 4)
sum_df_4 = sum_df_4.iloc[num]  #delete fallow index

sum_df_4["HWAH"]

#190115 visualize the yield of 30 years of SGX file.
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)

ax.bar(np.arange(1986, 2016), sum_df_4["HWAH"].values, color="red")

#plt.legend(loc="best", fontsize=14)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)        
ax.set_title("The Yield of Organic Rice in 30 years in Thailand", fontsize=16)
ax.set_xlabel("Year", fontsize=15)
ax.set_ylabel("Yield (kg/ha)", fontsize=15)
plt.savefig("181224_SSKT8601_SQX/190115_Yield_of_Organic_rice_SSKT9603.png", bbox_inches="tight")

plt.show()



#elnino data
elnino = [1987, 1991, 1997, 2002, 2009, 2014]
lanina = [1988, 1995, 1999, 2007, 2010]
hwah = sum_df_s["HWAH"].values

#visualize the impact of elnino and lanina to the weather.
fig = plt.figure(figsize = (12, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(1986, 2015):
    num = repr(i)[2:]
    df = searchElementforX(sskt, '^'+num)
    if len(list(filter(lambda x: re.search("\d{2}"+repr(i)[2:], x), 
                       np.asarray(elnino).astype(str)))):                
        ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
                color="red")
    
    elif len(list(filter(lambda x: re.search("\d{2}"+repr(i)[2:], x), 
                         np.asarray(lanina).astype(str)))): 
        ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
                color="blue")
        
    else:
        ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
                color="green")

nino, = plt.plot((0,0),(0,0), color="red", label="EL NINO")
nina, = plt.plot((0,0),(0,0), color="blue", label="LA NINA")
usual, = plt.plot((0,0),(0,0), color="green", label="USUAL")

plt.legend((nino, nina, usual), ("EL NINO", "LA NINA", "USUAL"), 
           loc='best', fontsize=14)

nino.set_visible(False)
nina.set_visible(False)
usual.set_visible(False)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Rain Fall (TPDOY=215)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Rain Fall (mm)', fontsize=15)
ax.set_xlim(200, 350)
#ax.set_ylim(0, 100)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()

        
"""
190114 generate dataframe for average, max, min value of each item
(['SRAD', 'TMAX', 'TMIN', 'RAIN', 'TAVE'])

1. The rule of index naming is like "1986_july_max"
2. The rule of columns naming is equal to ['SRAD', 'TMAX', 'TMIN', 'RAIN', 'TAVE']
"""


sskt = WTD2DataFrame("SSKT.WTD")
#generate index for dataframe
month = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
         "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
climate = ["general", "elnino", "lanina"]
ind = []
for i in range(1986, 2018):
    for j in range(len(month)):
        mi=repr(i)+"_"+month[j]+"_"+"min"
        ind.append(mi)
        ma=repr(i)+"_"+month[j]+"_"+"max"
        ind.append(ma)
        me=repr(i)+"_"+month[j]+"_"+"mean"
        ind.append(me)
        
sskt_stat = pd.DataFrame(index=ind, columns=sskt.columns)


#convert yydoy to yyyy-mm-dd
ind2 = []
for i in range(len(sskt.index)):
    if int(sskt.index[i][:2]) > 30:
        val = DOY2DATE(int(sskt.index[i][2:]), year=int("19"+sskt.index[i][:2]))
    else:
        val = DOY2DATE(int(sskt.index[i][2:]), year=int("20"+sskt.index[i][:2]))
    ind2.append(val)
    
sskt2 = pd.DataFrame(sskt.values, index=ind2, columns=sskt.columns)

#fill the sskt_stat dataframe
sskt_stat = pd.DataFrame(index=ind, columns=sskt.columns)
n = 0
for j in range(1986, 2018):
    ydf = searchElementforX(sskt2, repr(j))
    for k in range(len(month)):
        mdf = searchElementforX(ydf, repr(k+1)+"-\d{2}$")
        for i in range(len(sskt.columns)):
            sskt_stat.iloc[n,i] = min(mdf.iloc[:,i])
            sskt_stat.iloc[n+1,i] = max(mdf.iloc[:,i])
            sskt_stat.iloc[n+2,i] = mean(mdf.iloc[:,i])
        n = n+3
        
"""
190114 check the impact of elnino and lanina
Add the columns of "elnino or not" from 
"""
elnino = [1987, 1991, 1997, 2002, 2009, 2014]
lanina = [1988, 1995, 1999, 2007, 2010]
grow = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

climate = np.repeat("general", 8)
climate = np.append(climate, np.repeat("elnino", 17))
climate = np.append(climate, np.repeat("general", 2))
climate = np.append(climate, np.repeat("lanina", 14))
climate = np.append(climate, np.repeat("general", 22))
climate = np.append(climate, np.repeat("elnino", 16))
climate = np.append(climate, np.repeat("general", 35))
climate = np.append(climate, np.repeat("lanina", 8))
climate = np.append(climate, np.repeat("general", 13))
climate = np.append(climate, np.repeat("elnino", 14))
climate = np.append(climate, np.repeat("general", 2))
climate = np.append(climate, np.repeat("lanina", 21))
climate = np.append(climate, np.repeat("general", 25))
climate = np.append(climate, np.repeat("elnino", 9))
climate = np.append(climate, np.repeat("general", 31))
climate = np.append(climate, np.repeat("lanina", 6))
climate = np.append(climate, np.repeat("general", 12))
climate = np.append(climate, np.repeat("lanina", 13))
climate = np.append(climate, np.repeat("general", 13))
climate = np.append(climate, np.repeat("elnino", 10))
climate = np.append(climate, np.repeat("general", 3))
climate = np.append(climate, np.repeat("lanina", 9))
climate = np.append(climate, np.repeat("general", 38))
climate = np.append(climate, np.repeat("elnino", 23))
climate = np.append(climate, np.repeat("general", 16))
climate = np.append(climate, np.repeat("lanina", 4))

climate_df = pd.DataFrame(climate, index=searchElementforX(sskt_stat, "mean").index, 
                          columns=["climate"])

mean_df = pd.concat([searchElementforX(sskt_stat, "mean"), climate_df], axis=1, sort=True)

"""
#190115 generate bar graph for the rainfall average in each month.
1. prepare dataframe for average value
2. visualize
"""
#1
bar_df_rain = pd.DataFrame(index=month, columns=climate)

for i in range(len(month)):
    df = searchElementforX(mean_df, month[i])
    for j in range(len(climate)):
        cli = df[df["climate"]==climate[j]]
        rain = cli["RAIN"].values
        bar_df_rain.iloc[i,j] = mean(rain)
        
#2
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(len(climate)):
    ax.bar(np.arange(len(bar_df_rain.index))+n, bar_df_rain.iloc[:,i],
           width=0.8/len(climate), color=cm.hsv(i/len(climate)), label=climate[i])
    n=n+0.8/len(climate)
    
plt.legend(loc="best", fontsize=14)
plt.xticks(np.arange(len(bar_df_rain.index))+0.35, month, fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)        
ax.set_title("EL NINO and LA NINA inpact against RAINFALL", fontsize=16)
ax.set_xlabel("month", fontsize=15)
ax.set_ylabel("Average daily rainfall(mm)", fontsize=15)

plt.show()


"""
#190115 generate bar graph for the solar radiation average in each month.
1. prepare dataframe for average value
2. visualize
"""
#1
bar_df_srad = pd.DataFrame(index=month, columns=climate)

for i in range(len(month)):
    df = searchElementforX(mean_df, month[i])
    for j in range(len(climate)):
        cli = df[df["climate"]==climate[j]]
        rain = cli["SRAD"].values
        bar_df_srad.iloc[i,j] = mean(rain)
        
#2
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(len(climate)):
    ax.bar(np.arange(len(bar_df_srad.index))+n, bar_df_srad.iloc[:,i],
           width=0.8/len(climate), color=cm.hsv(i/len(climate)), label=climate[i])
    n=n+0.8/len(climate)
    
plt.legend(loc="best", fontsize=14)
plt.xticks(np.arange(len(bar_df_srad.index))+0.35, month, fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)        
ax.set_title("EL NINO and LA NINA inpact against Solar Radiation", fontsize=16)
ax.set_xlabel("month", fontsize=15)
ax.set_ylabel("Daily Solar Radiation(MJ/m2)", fontsize=15)

plt.show()


"""
#190115 generate bar graph for the average temperature in each month.
1. prepare dataframe for average value
2. visualize
"""
#1
bar_df_tave = pd.DataFrame(index=month, columns=climate)

for i in range(len(month)):
    df = searchElementforX(mean_df, month[i])
    for j in range(len(climate)):
        cli = df[df["climate"]==climate[j]]
        rain = cli["TAVE"].values
        bar_df_tave.iloc[i,j] = mean(rain)
        
#2
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(len(climate)):
    ax.bar(np.arange(len(bar_df_tave.index))+n, bar_df_tave.iloc[:,i],
           width=0.8/len(climate), color=cm.hsv(i/len(climate)), label=climate[i])
    n=n+0.8/len(climate)
    
plt.legend(loc="best", fontsize=14)
plt.xticks(np.arange(len(bar_df_tave.index))+0.35, month, fontsize=14)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)        
ax.set_title("EL NINO and LA NINA inpact against Average temperature", fontsize=16)
ax.set_xlabel("month", fontsize=15)
ax.set_ylabel("Average Temperature(celcius)", fontsize=15)

plt.show()


















