#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  7 08:28:28 2019

@author: kameokashinichi
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil
from pylab import cm

"""
190104_Dssat spil-water relation file
http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/cropsim/exec/2019-01-06T09-58-44-971Z578b8a33e98d22b2
soilid -> "JP_NRAL01A"

soilWat.OUT, Summary.OUT, SoilNi.OUT, PlantN.OUT, 100 weather scenarios
"""
"""
190107 read water stress Dssat file.(SoilWat.OUT)
"""

soilW = []
with open(os.getcwd() + '/2019-01-06T09-58-44-971Z578b8a33e98d22b2/SoilWat.OUT', 'r') as f:
    for row in f:
        soilW.append(row.strip())
        
soilW = soilW[12:]        

#separate each rows by empty letter        
stress = []     
for row in soilW:
    element = row.split()
    stress.append(element)   
        
columns = stress[0]

#extract available rows
stress = np.asarray(stress)
num = []
for i in range(len(stress)):
    if stress[i] == columns:
        pass
    elif len(stress[i]) != 21:
        pass
    else:
        num.append(i)

sw = stress[num]

"""
for i in range(len(sw)):
    if len(sw[i]) != 21:
        print(i)
"""

#convert list to np.array    
s_stress = []
for i in range(len(sw)):
    s_stress.append(sw[i])
s_stress = np.asarray(s_stress)    

sw_df = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = s_stress[:,0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(sw_df.index)):
    if i == len(sw_df.index)-1:
        break
    elif int(sw_df.iloc[i, 0]) > int(sw_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(sw_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
sw_df2 = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)
 
"""
190106 Summary.OUT
"""
record = []
with open(os.getcwd() + '/2019-01-06T09-58-44-971Z578b8a33e98d22b2/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df2 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

"""
190106 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-06T09-58-44-971Z578b8a33e98d22b2/SoilNi.OUT', 'r') as f:
    for row in f:
        soilN.append(row.strip())
        
soilN = soilN[12:]        

#separate each rows by empty letter        
stressN = []     
for row in soilN:
    element = row.split()
    stressN.append(element)   
        
columns = stressN[0]

#extract available rows
stressN = np.asarray(stressN)
num = []
for i in range(len(stressN)):
    if stressN[i] == columns:
        pass
    elif len(stressN[i]) != 28:
        pass
    else:
        num.append(i)
sn = stressN[num]

"""
for i in range(len(sn)):
    if len(sn[i]) != 28:
        print(i)
"""

#convert list to np.array
sn_stress = []
for i in range(len(sn)):
    sn_stress.append(sn[i])
sn_stress = np.asarray(sn_stress)

sn_df = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = sn_stress[:, 0])    

#change the index from year to simulation number
number = [0]
for i in range(len(sn_df.index)):
    if i == len(sn_df.index)-1:
        break
    elif int(sn_df.iloc[i, 0]) > int(sn_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(sn_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
sn_df2 = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = newcol)    

"""
190106 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-06T09-58-44-971Z578b8a33e98d22b2/PlantN.OUT', 'r') as f:
    for row in f:
        PN.append(row.strip())
        
PN = PN[10:]

#separate each rows by empty letter        
stressPN = []     
for row in PN:
    element = row.split()
    stressPN.append(element)   
        
columns = stressPN[0]

#extract available rows
stressPN = np.asarray(stressPN)
num = []
for i in range(len(stressPN)):
    if stressPN[i] == columns:
        pass
    elif len(stressPN[i]) != 18:
        pass
    else:
        num.append(i)
        
pn = stressPN[num]
"""
for i in range(len(pn)):
    if len(pn[i]) != 18:
        print(i)
"""

#convert list to np.array
pn_stress = []
for i in range(len(pn)):
    pn_stress.append(pn[i])
pn_stress = np.asarray(pn_stress)

#convert np.ndarray to pd.DataFrame
pn_df = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = pn_stress[:, 0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(pn_df.index)):
    if i == len(pn_df.index)-1:
        break
    elif int(pn_df.iloc[i, 0]) > int(pn_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(pn_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
pn_df2 = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = newcol)


#classify THE soil water GRAPH BY ANNUAL YIELD
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

hwah = sum_df2["HWAH"].values.astype(np.int32)

n = 0
for i in range(1, 30):
    im = ax.plot(sw_df2.loc[:, 'DOY'][sw_df2.index == i].values.astype(np.int32), 
            sw_df2.loc[:, 'SWTD'][sw_df2.index == i].values.astype(np.int32),
            color=cm.RdBu(hwah[i-1]/max(hwah)), label=repr(i)+'(y='+repr(hwah[i-1])+')')
    
plt.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Total soil water content(mm)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Total soil water in profile(mm)', fontsize=15)
#ax.set_ylim(0, 410)
#ax.set_xlim(0, 365)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_water_with_yield_RIX', bbox_inches='tight')
plt.show()


#classify THE Soil N GRAPH BY ANNUAL YIELD
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

for i in range(20, 35):
    ax.plot(sn_df2.loc[:, 'DOY'][sn_df2.index == i].values.astype(np.int32), 
            sn_df2.loc[:, 'NI1D'][sn_df2.index == i].values.astype(np.float64),
            color=cm.RdBu(hwah[i-1]/max(hwah)), label=repr(i)+'(y='+repr(hwah[i-1])+')')
    
plt.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Total soil N content(TPDOY=194)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Total soil N in profile(kg/ha)', fontsize=15)
#ax.set_ylim(5, 105)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_total_NO2_with_yield_RIX, bbox_inches='tight')
plt.show()

#classify THE Soil N leaching(NLCC) GRAPH BY ANNUAL YIELD
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, 12):
    ax.plot(sn_df2.loc[:, 'DOY'][sn_df2.index == i].values.astype(np.int32), 
            sn_df2.loc[:, 'NLCC'][sn_df2.index == i].values.astype(np.float64),
            color=cm.RdBu(hwah[i-1]/max(hwah)), label=repr(i)+'(y='+repr(hwah[i-1])+')')
    
plt.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Total soil N leaching(TPDOY=194)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Daily soil N leaching(kg/ha)', fontsize=15)
#ax.set_ylim(5, 105)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_total_NO2_with_yield_RIX, bbox_inches='tight')
plt.show()




#the relationship between rainfall and yield   
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

for i in range(1, 20):
    weath = searchElementforX(wlis[i-1], '^18')
    ax.plot(np.arange(1, len(weath.index)+1, 1), 
            weath.loc[:, 'RAIN'].values.astype(np.float64),
            color=cm.RdBu(hwah[i-1]/max(hwah)), 
            label=repr(i)+'(y='+repr(hwah[i-1])+')')
    
plt.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Rainfall VS Yield", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Daily rainfall(mm)', fontsize=15)
ax.set_ylim(5, 120)
ax.set_xlim(200, 250)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_total_NO2_with_yield_RIX, bbox_inches='tight')
plt.show()


#correlation between yield and NO3(DOY230)
#relation between yield and surface NO3
juv_no1 = sn_df2[sn_df2["DOY"]=="245"]
uni = []
for i in range(len(juv_no1.index)):
    if i == 0:
        uni.append(i)
    elif juv_no1.index[i] != juv_no1.index[i-1]:
        uni.append(i)
    else:
        pass

juv_no1_uni = juv_no1.iloc[uni]

fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

no3 = juv_no1_uni["NI1D"].values.astype(np.float64)
hwah4 = sum_df2.loc[:, 'HWAH'].values.astype(np.int32)   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS70) VS Yield", fontsize=18)
plt.xlabel('NO3 content in surface layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/190105_NH4_surface_in_DAS0_VS_yield_SSKT9601.png')

plt.show()


#plot rainfall and soil N content
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

for i in range(1, 5):
    weath = searchElementforX(wlis[i-1], '^18')
    ax.plot(sn_df2.loc[:, 'DOY'][sn_df2.index == i].values.astype(np.int32), 
            sn_df2.loc[:, 'NI1D'][sn_df2.index == i].values.astype(np.float64),
            color=cm.hsv((i-1)/4), label="soil"+repr(i)+'(y='+repr(hwah[i-1])+')')
    ax2.plot(np.arange(1, len(weath.index)+1, 1), 
            weath.loc[:, 'RAIN'].values.astype(np.float64),
            color=cm.hsv((i-1)/4))
    
ax.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Total soil N content(TPDOY=213)", fontsize=18)
ax.set_xlabel('Day of year', fontsize=15)
ax.set_ylabel('Total soil N in profile(kg/ha)', fontsize=15)
ax2.set_ylabel('Daily rainfall(mm)', fontsize=15)
ax.set_ylim(0, 105)
ax.set_xlim(200, 250)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_total_NO2_with_yield_RIX, bbox_inches='tight')
plt.show()


#plant N flow in single year
order = sum_df2.sort_values("HWAH").index
#vixualize the soil N movement in single year(low yield case)
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

wnum = int(order[8])

dfs = sn_df2[sn_df2.index == wnum]
dfp = pn_df2[pn_df2.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI2D'].values.astype(np.float64), 
        color='orange')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'VNAD'].values.astype(np.float64),
        color='green')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'CNAD'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax2.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
top, = plt.plot((1,2), (2,2), color="red", linewidth=10)
plant, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, top, plant, rain), ('soil NO3 (15cm)', 'soil NO3', 'plant', 'top', 'rain'),
           loc="best", fontsize=14)

nh.set_visible(False)
no.set_visible(False)
top.set_visible(False)
plant.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+sum_df2.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


#plant N flow in single year
#vixualize the soil N movement in single year(high yield case)
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

wnum = int(order[90])

dfs = sn_df2[sn_df2.index == wnum]
dfp = pn_df2[pn_df2.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI2D'].values.astype(np.float64), 
        color='orange')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'VNAD'].values.astype(np.float64),
        color='green')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'CNAD'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax2.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
top, = plt.plot((1,2), (2,2), color="red", linewidth=10)
plant, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, top, plant, rain), ('soil NO3 (15cm)', 'soil NO3', 'plant', 'top', 'rain'),
           loc="best", fontsize=14)

nh.set_visible(False)
no.set_visible(False)
top.set_visible(False)
plant.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No"+repr(wnum)+"(yield="+sum_df2.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(150, 300)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

"""
#visualize multi layer soil NH4 status.
"""
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

wnum = int(order[92])

dfs = sn_df2[sn_df2.index == wnum]
#dfp = pn_df2[pn_df2.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NH1D'].values.astype(np.float64), 
        color='brown')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NH2D'].values.astype(np.float64), 
        color='orange')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NH3D'].values.astype(np.float64),
        color='green')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NH4D'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NH5D'].values.astype(np.float64), 
        color = 'blue')

no1, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no2, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
no3, = plt.plot((1,2), (2,2), color="red", linewidth=10)
no4, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
no5, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((no1, no2, no3, no4, no5), ('NH4 surface', 'NH4 15cm', 'NH4 30cm', 'NH4 40cm', 'NH4 50cm'),
           loc="best", fontsize=14)

no1.set_visible(False)
no2.set_visible(False)
no3.set_visible(False)
no4.set_visible(False)
no5.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No"+repr(wnum)+"(yield="+sum_df2.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(150, 300)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

"""
190107 visualize multi layer soil NO3 status.
"""
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

wnum = int(order[92])

dfs = sn_df2[sn_df2.index == wnum]
#dfp = pn_df2[pn_df2.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI2D'].values.astype(np.float64), 
        color='orange')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI3D'].values.astype(np.float64),
        color='green')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI4D'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI5D'].values.astype(np.float64), 
        color = 'blue')

no1, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no2, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
no3, = plt.plot((1,2), (2,2), color="red", linewidth=10)
no4, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
no5, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((no1, no2, no3, no4, no5), ('NO3 surface', 'NO3 15cm', 'NO3 30cm', 'NO3 40cm', 'NO3 50cm'),
           loc="best", fontsize=14)

no1.set_visible(False)
no2.set_visible(False)
no3.set_visible(False)
no4.set_visible(False)
no5.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No"+repr(wnum)+"(yield="+sum_df2.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 330)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

#visualize the soil surface NO3 status in terms of the yield
order = sum_df2.sort_values("HWAH").index

fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

for i in range(4):
    wnum = int(order[i])
    ni1d = sn_df2.loc[:, 'NI1D'][sn_df2.index == wnum].values.astype(np.float32)
    doy = sn_df2.loc[:, 'DOY'][sn_df2.index == wnum].values.astype(np.int32)
    ax.plot(doy, ni1d, color = 'blue')
for i in range(96,100):
    wnum = int(order[i])
    ni1d = sn_df2.loc[:, 'NI1D'][sn_df2.index == wnum].values.astype(np.float32)
    doy = sn_df2.loc[:, 'DOY'][sn_df2.index == wnum].values.astype(np.int32)
    ax.plot(doy, ni1d, color = 'red')
   

low, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
high, = plt.plot((1,2), (2,2), color="red", linewidth=10)

plt.legend((low, high), ('Low Yield', "High Yield"),
           loc="best", fontsize=14)

low.set_visible(False)
high.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("Daily soil surface NO3(kg/ha)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Surface soil NO3 content sorted by the yield", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 330)
#ax.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190107 visualize the weather sorted by the yield
"""
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

wnum = int(order[0])
for i in range(len(wlis[wnum-1].columns)):
    prop = searchElementforX(wlis[wnum-1], '^18').iloc[:, i].values
    ax.plot(np.arange(1, len(prop)+1, 1), prop, 
            color=cm.hsv(i/len(wlis[wnum-1].columns)),
            label=wlis[wnum-1].columns[i])

plt.legend(loc='best', fontsize=13)
#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("rain(mm), srad(MJ/m2), tmax and tmin(cel)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Weather property of the scenario No"+repr(wnum)+"(yield="+sum_df2.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(150, 300)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190107 categorize the best5 and worst5 weather scenario.
"""
order = sum_df2.sort_values("HWAH").index

fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

for i in range(8):
    wnum = int(order[i])
    prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
    ax.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')
for i in range(92,100):
    wnum = int(order[i])
    prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
    ax.plot(np.arange(1, len(prep)+1, 1), prep, color = 'red')
   

low, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
high, = plt.plot((1,2), (2,2), color="red", linewidth=10)

plt.legend((low, high), ('Low Yield', "High Yield"),
           loc="best", fontsize=14)

low.set_visible(False)
high.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("Daily rainfall amount(mm)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Rainfall compared in terms of the yield", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(260, 290)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

"""
190107 rain fall in the juvenile, vegetative growth season
"""
rain = []
for i in range(100):
    df = searchElementforX(wlis[i], '^18')
    tor = sum(df.loc["18275":"18277", "RAIN"])
    rain.append(tor)

#check the correlation between PRCP(precipitation during juvenile) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(rain)
hwah4 = sum_df2.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Precipitation of DAS 50-60 VS Yield", fontsize=18)
plt.xlabel('Precipitation(50-60 days after seeding) (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()



#check the correlation between PRCP(precipitation during planting) and HWAH
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = sum_df2.loc[:, 'PRCP'].values.astype(np.float32)
hwah4 = sum_df2.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Precipitation VS Yield", fontsize=18)
plt.xlabel('Precipitation during cultivation (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()

"""
190107 soil water content(SW1D cm3/cm3) VS yield
"""

order = sum_df2.sort_values("HWAH").index

fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

for i in range(4):
    wnum = int(order[i])
    swtd = sw_df2.loc[:, 'SW2D'][sw_df2.index == wnum].values.astype(np.float32)
    doy = sw_df2.loc[:, 'DOY'][sw_df2.index == wnum].values.astype(np.int32)
    ax.plot(doy, swtd, color = 'blue')
for i in range(96,100):
    wnum = int(order[i])
    swtd = sw_df2.loc[:, 'SW2D'][sw_df2.index == wnum].values.astype(np.float32)
    doy = sw_df2.loc[:, 'DOY'][sw_df2.index == wnum].values.astype(np.int32)
    ax.plot(doy, swtd, color = 'red')
   

low, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
high, = plt.plot((1,2), (2,2), color="red", linewidth=10)

plt.legend((low, high), ('Low Yield', "High Yield"),
           loc="best", fontsize=14)

low.set_visible(False)
high.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("Daily soil surface WC(cm3/cm3)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Water content sorted by the yield", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 230)
ax.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


#check the correlation between WC-15cm(cm3/cm3) in DOY200 and HWAH
doy = sw_df2.loc[:, 'DOY'].values.astype(np.int32).reshape(-1, 1)
sw2d = sw_df2.loc[:, 'SW2D'].values.astype(np.float32).reshape(-1, 1)
swdoy = np.concatenate((doy,sw2d), axis=1)
swdoy_df = pd.DataFrame(swdoy, index=sw_df2.index, columns=["DOY", "SW2D"])
wc = []
for i in range(1, 101):
    df = swdoy_df[sw_df2.index == i]
    ave = mean(df.query("192 < DOY <207")["SW2D"])
    wc.append(ave)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(wc)
hwah4 = sum_df2.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("WC in DOY200 VS Yield", fontsize=18)
plt.xlabel('Water Content in DOY192-207 (cm3/cm3)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/190107_WC_15cm_DOY192_207_VS_Yield_JPSOIL_SSKT.png', bbox_inches='tight')

plt.show()

"""
190107 generate principal component analysis
the properties are:
1. Yield of each weather scenario
2. Soil Water content in 15cm layer during DOY192-207
3. soil surface NO3 content
"""











