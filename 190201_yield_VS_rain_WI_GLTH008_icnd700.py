#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 10:01:48 2019

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
from mpl_toolkits.mplot3d import Axes3D
from sklearn import linear_model

"""
190125 Check the sensitivity of "icrt", "icnd" and "icres" against Final Yield.

     No1 No2 No3 No4 No5 No6 No7 No8 No9
icres  0   0   0 100 400 700   0   0   0
icrt 100 400 700   0   0   0   0   0   0
icnd   0   0   0   0   0   0 100 400 700

No1 -> "2019-01-25T09-32-55-312Z659a00f91b5791cc"
No2 -> "2019-01-25T09-38-16-204Z51340cc5356b47cc"
No3 -> "2019-01-25T09-41-26-888Z4684f999972c214f"
No4 -> "2019-01-25T09-44-12-143Zb07b705502e84ab4"
No5 -> "2019-01-25T09-46-08-296Zdb4e3766c50ae5cf"
No6 -> "2019-01-25T09-48-17-311Z31caaaaa9c33ce70"
No7 -> "2019-01-25T09-51-02-833Zcc844e47f6fb70f5"
No8 -> "2019-01-25T09-53-13-820Z80b76f99a531cce7"
No9 -> "2019-01-25T09-54-56-147Z5e9f249085717d6b"

Soil ID -> "WI_GLTH008"
ICDAT -> 18182
PDATE -> 18194(Transpanting)
ICREN -> 2.8
RAMT -> 600
Initial soil condition
@C  ICBL  SH2O  SNH4  SNO3
 1     5   .05  2.50  7.14
 1    15   .07  2.57  4.66
 1    30   .05  0.04  3.88
 1    42   .04  0.07  3.71
 1    55   .04  0.03  1.37
 1    67   .05  0.01  0.98
 1    80   .07  0.01  1.06
 1   100   .05  0.01  1.231

Conclusion:
    The sensitivity of icnd is the biggest.
"""


"""
190201 Check relation between weather and yield of No9
"""

#sum9(No9)
record = []
with open(os.getcwd() + '/2019-01-25T09-54-56-147Z5e9f249085717d6b/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum9 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

y_value = sum9.loc[:, ["ADAT","MDAT","HWAH"]].values.astype(np.int32)
sum_df = pd.DataFrame(y_value, index=sum9.index, columns=["ADAT","MDAT","HWAH"])

"""
190201 read 100 weather file (WTDE) of SSKT
"""
lis = os.listdir(os.getcwd()+"/2019-01-05T08-02-58-215Z9de7b566152a6862")
WTDE = list(filter(lambda x: re.search('.WTDE', x), lis))
WTDE.sort()

wlis = []
for i in WTDE:
    a = WTD2DataFrame("/2019-01-05T08-02-58-215Z9de7b566152a6862/"+i)
    wlis.append(a)


"""
190201 SoilWat.OUT
"""
soilW = []
with open(os.getcwd() + '/2019-01-25T09-54-56-147Z5e9f249085717d6b/SoilWat.OUT', 'r') as f:
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
    elif len(stress[i]) != 23:
        pass
    else:
        num.append(i)

sw = stress[num]

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
    
sw_df5 = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)


"""
190201 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-25T09-54-56-147Z5e9f249085717d6b/PlantN.OUT', 'r') as f:
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
    
pn_df5 = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = newcol)

"""
190201 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-25T09-54-56-147Z5e9f249085717d6b/SoilNi.OUT', 'r') as f:
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
    elif len(stressN[i]) != 32:
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
    
sn_df5 = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = newcol) 

"""
190201 the relation between rainy day (in particular duration) and yield
"""
rain_day = []
for i in range(100):        
    prep = searchElementforX(wlis[i], "^18")["RAIN"].values.astype(np.float32)
    a = 0
    for j in range(195, 220):
        if prep[j] > 20:
            a = a + 1
            
    rain_day.append(a)

#visualize the relationship between rainy day in juvenile stage and yield
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

rain = np.asarray(rain_day)
hwah4 = sum_df.loc[:, 'HWAH'].values.astype(np.int32)   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = rain.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(rain, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),rain,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("amount of rainy days(more than 20mm/day) VS Yield -WI_GLTH008_icnd=700kg/ha-", fontsize=18)
plt.xlabel('Number of rainy days during DOY195-220', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('190108_Reiton_RIX_png/190201_rainy_days_195_220doy_VS_yield_WI_GLTH008_No9.png')

plt.show()

"""
190201 check the single year's rainfall and yield.
"""

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

wnum = 99

prep = searchElementforX(wlis[wnum-1], "^18")["RAIN"].values.astype(np.float32)
hwah = sum_df.loc[repr(wnum), 'HWAH']

ax2.plot(np.arange(0, len(prep)), prep, color="blue", label="Rain")
ax.plot((0, len(prep)), (hwah,hwah), color="red", label="Yield")

plt.legend(fontsize=14, loc="best")
ax.set_ylabel("Yield(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+repr(hwah)+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190201 compare the rainfall pattern of several scenarios
"""

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

order = sum_df.sort_values("HWAH").index.values.astype(np.int32)
#wnum = order[[1,50,80]]
wnum = [83, 97, 94]

for i in range(len(wnum)):
    prep = searchElementforX(wlis[wnum[i]-1], "^18")["RAIN"].values.astype(np.float32)
    hwah = sum_df.loc[repr(wnum[i]), 'HWAH']    
    ax.plot(np.arange(0, len(prep)), prep, color=cm.hsv(i/len(wnum)), label="No"+repr(wnum[i])+"(Yield="+repr(hwah)+"kg/ha)")


plt.legend(fontsize=14, loc="best")
ax.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Daily rainfall of the scenario", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190201 single year's plant N and precipitation.
"""

fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

#wnum = int(order1[90])
wnum = 83

dfs = sn_df5[sn_df5.index == wnum]
dfp = pn_df5[pn_df5.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI2D'].values.astype(np.float64), 
        color='orange')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'CNAD'].values.astype(np.float64),
        color='green')
ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
        dfp.loc[:, 'GNAD'].values.astype(np.float64), 
        color='red')
#ax.plot(dfp.loc[:, 'DOY'], dfp.loc[:, 'GNAD'], color='blue', label='grain')
ax2.plot(np.arange(1, len(prep)+1, 1), prep, color = 'blue')

nh, = plt.plot((1,2), (2,2), color="orange", linewidth=10)
no, = plt.plot((1,2), (2,2), color="brown", linewidth=10)
grain, = plt.plot((1,2), (2,2), color="red", linewidth=10)
top, = plt.plot((1,2), (2,2), color="green", linewidth=10)
#grain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
rain, = plt.plot((1,2), (2,2), color="blue", linewidth=10)

plt.legend((nh, no, grain, top, rain), ('soil NO3 (15cm)', 'soil NO3', 'grain', 'top', 'rain'),
           loc="best", fontsize=14)

nh.set_visible(False)
no.set_visible(False)
top.set_visible(False)
grain.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+repr(sum_df.loc[repr(wnum),"HWAH"])+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

"""
190201 compare the plant N pattern of several scenarios
"""
fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

order = sum_df.sort_values("HWAH").index.values.astype(np.int32)
#wnum = order[[1,50,80]]
wnum = [83, 97, 94]

for i in range(len(wnum)):
    dfp = pn_df5[pn_df5.index == wnum[i]]
    hwah = sum_df.loc[repr(wnum[i]), 'HWAH']    
    ax.plot(dfp.loc[:, 'DOY'].values.astype(np.int32), 
            dfp.loc[:, 'CNAD'].values.astype(np.float64),
            color=cm.hsv(i/len(wnum)),
            label="No"+repr(wnum[i])+"(Yield="+repr(hwah)+"kg/ha)")

plt.legend(fontsize=14, loc="best")
ax.set_ylabel('Plant N amount(kg/ha)', fontsize=15)
plt.title("Movement of Plant N", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190201 rain fall in the juvenile, vegetative growth season
"""
rain = []
for i in range(100):
    df = searchElementforX(wlis[i], '^18')
    tor = sum(df.loc["18195":"18215", "RAIN"])
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







