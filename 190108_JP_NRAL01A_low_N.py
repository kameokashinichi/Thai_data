#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 09:03:23 2019

@author: kameokashinichi
"""

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil
from pylab import cm
from statistics import mean, stdev, median
from sklearn import linear_model

"""
190108_Dssat spil-water relation file
http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/cropsim/exec/2019-01-07T08-44-50-175Z91c5fafc7bf84065
soilID -> "JP_NRAL01A" low nutrient status

soilWat.OUT, Summary.OUT, SoilNi.OUT, PlantN.OUT, 100 weather scenarios
"""
"""
190108 read water stress Dssat file.(SoilWat.OUT)
"""

soilW = []
with open(os.getcwd() + '/2019-01-07T08-44-50-175Z91c5fafc7bf84065/SoilWat.OUT', 'r') as f:
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
    
sw_df4 = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)
 
"""
190106 Summary.OUT
"""
record = []
with open(os.getcwd() + '/2019-01-07T08-44-50-175Z91c5fafc7bf84065/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df4 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

"""
190106 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-07T08-44-50-175Z91c5fafc7bf84065/SoilNi.OUT', 'r') as f:
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
    
sn_df4 = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = newcol)    

"""
190106 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-07T08-44-50-175Z91c5fafc7bf84065/PlantN.OUT', 'r') as f:
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
    
pn_df4 = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = newcol)


"""
190108 analyze the relation between yield(HWAH) and surface NO3(NI1D)
"""
info = sum_df4.loc[:, ["HDAT","HWAH", "PRCP"]].values.astype(np.float32)
sum_df4_1 = pd.DataFrame(info, index=sum_df4.index, columns=["HDAT","HWAH", "PRCP"])

order1 = sum_df4_1.sort_values("HWAH")["HWAH"].index

juv_no1 = sn_df4[sn_df4["DOY"]=="255"]
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
hwah4 = sum_df4.loc[:, 'HWAH'].values.astype(np.int32)   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),no3,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS61) VS Yield", fontsize=18)
plt.xlabel('NO3 content in surface layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('190108_Reiton_RIX_png/190108_NH4_surface_in_DAS61_VS_yield_HC_GEN0005.png')

plt.show()

"""
190108 Relationship among rain, soil water(SW1D,SW2D,SW3D) and soilN(NI1D,NH1D).
-> in this soil, If the water volume become above full, the NO3 is leaching
"""
order1 = sum_df4_1.sort_values("HWAH")["HWAH"].index

fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

wnum = int(order1[50])

dfw = sw_df4[sn_df4.index == wnum]
dfs = sn_df4[sn_df4.index == wnum]
dfp = pn_df4[pn_df4.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax2.plot(dfw.loc[:, 'DOY'].values.astype(np.int32), 
        dfw.loc[:, 'SWTD'].values.astype(np.float64),
        color='orange')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'CNAD'].values.astype(np.float64),
        color='green')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'GNAD'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
sw, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
top, = plt.plot((1,2), (2,2), color="green", linewidth=10)
grain, = plt.plot((1,2), (2,2), color="red", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((no, sw, top, grain, rain), ('soil NO3', 'soil WC', 'top', 'grain', 'rain'),
           loc="best", fontsize=14)

no.set_visible(False)
sw.set_visible(False)
top.set_visible(False)
grain.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha), daily rainfall(mm)", fontsize=15)
ax2.set_ylabel('Soil water content(cm3/cm3)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+sum_df4.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
#ax2.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190108_N_and_water_flow_JP_NRAL01A.png', bbox_inches='tight')
plt.show()


























