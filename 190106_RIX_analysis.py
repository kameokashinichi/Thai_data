#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jan  6 07:44:09 2019

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
http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/cropsim/exec/2019-01-05T08-02-58-215Z9de7b566152a6862/
soilWat.OUT, Summary.OUT, SoilNi.OUT, PlantN.OUT, 100 weather scenarios
"""
"""
190106 read water stress Dssat file.(SoilWat.OUT)
"""
soilW = []
with open(os.getcwd() + '/2019-01-05T08-02-58-215Z9de7b566152a6862/SoilWat.OUT', 'r') as f:
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

for i in range(len(sw)):
    if len(sw[i]) != 23:
        print(i)

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
    
sw_df = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)
 
"""
190106 Summary.OUT
"""
record = []
with open(os.getcwd() + 'Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

"""
190106 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-05T08-02-58-215Z9de7b566152a6862/SoilNi.OUT', 'r') as f:
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
    if len(sn[i]) != 32:
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
    
sn_df = pd.DataFrame(sn_stress[:, 1:], columns=columns[1:], index = newcol)    

"""
190106 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-05T08-02-58-215Z9de7b566152a6862/PlantN.OUT', 'r') as f:
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
    
pn_df = pd.DataFrame(pn_stress[:, 1:], columns=columns[1:], index = newcol)

"""
190106 read 100 weather file (WTDE)
"""
lis = os.listdir(os.getcwd()+"/2019-01-05T08-02-58-215Z9de7b566152a6862")
WTDE = list(filter(lambda x: re.search('.WTDE', x), lis))
WTDE.sort()

wlis = []
for i in WTDE:
    a = WTD2DataFrame("/2019-01-05T08-02-58-215Z9de7b566152a6862/"+i)
    wlis.append(a)
    

#classify THE soil water GRAPH BY ANNUAL YIELD
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

hwah = sum_df["HWAH"].values.astype(np.int32)

n = 0
for i in range(1, 30):
    im = ax.plot(sw_df.loc[:, 'DOY'][sw_df.index == i].values.astype(np.int32), 
            sw_df.loc[:, 'SWTD'][sw_df.index == i].values.astype(np.int32),
            color=cm.RdBu(hwah[i-1]/max(hwah)), label=repr(i)+'(y='+repr(hwah[i-1])+')')
    
#plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Total soil water content(mm)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Total soil water in profile(mm)', fontsize=15)
ax.set_ylim(0, 410)
#ax.set_xlim(0, 365)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_water_with_yield_RIX', bbox_inches='tight')
plt.show()


#classify THE Soil N GRAPH BY ANNUAL YIELD
fig = plt.figure(figsize = (8, 6))
ax = fig.add_subplot(1,1,1)

for i in range(20, 35):
    ax.plot(sn_df.loc[:, 'DOY'][sn_df.index == i].values.astype(np.int32), 
            sn_df.loc[:, 'NI2D'][sn_df.index == i].values.astype(np.float64),
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
    ax.plot(sn_df.loc[:, 'DOY'][sn_df.index == i].values.astype(np.int32), 
            sn_df.loc[:, 'NLCC'][sn_df.index == i].values.astype(np.float64),
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
juv_no1 = sn_df[sn_df["DOY"]=="255"]
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
hwah4 = sum_df.loc[:, 'HWAH'].values.astype(np.int32)   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS60) VS Yield", fontsize=18)
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
    ax.plot(sn_df.loc[:, 'DOY'][sn_df.index == i].values.astype(np.int32), 
            sn_df.loc[:, 'NI1D'][sn_df.index == i].values.astype(np.float64),
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
ax.set_ylim(5, 105)
ax.set_xlim(200, 250)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#plt.savefig('181224_Dssat_png/190106_soil_total_NO2_with_yield_RIX, bbox_inches='tight')
plt.show()












"""
181204 plantgro.out
"""
#read Plant growth Dssat file.
PG = []
with open(os.getcwd() + '/' + 'PlantGro.OUT', 'r') as f:
    for row in f:
        PG.append(row.strip())
        
PG = PG[13:]

#separate each rows by empty letter        
stressPG = []     
for row in PG:
    element = row.split()
    stressPG.append(element)   
        
columns = stressPG[0]

#extract available rows
stressPG = np.asarray(stressPG)
num = []
for i in range(len(stressPG)):
    if stressPG[i] == columns:
        pass
    elif len(stressPG[i]) != 36:
        pass
    else:
        num.append(i)
        
pg = stressPG[num]

for i in range(len(pg)):
    if len(pg[i]) != 36:
        print(i)

#convert list to np.array(https://deepage.net/features/numpy-append.html, https://note.nkmk.me/python-numpy-dtype-astype/)
pg_stress = []
for i in range(len(pg)):
    pg_stress.append(pg[i])
pg_stress = np.asarray(pg_stress)

#convert np.ndarray to pd.DataFrame
pg_df = pd.DataFrame(pg_stress[:, 1:], columns=columns[1:], index = pg_stress[:, 0])    

#check the number of each simulation(1-5)    
for i in range(len(pg_df.index)):
    if i == len(pg_df.index) - 1:
        print(i)
        break
    elif pg_df.index[i] == '2017' and pg_df.index[i] != pg_df.index[i+1]:
        print(i)
    else:
        pass

#dataframe for simulation No1 
pg_df_1 = pg_df.iloc[:3526, :]

#classify THE GRAPH BY ANNUAL YIELD(Tiller number)
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    im = ax.plot(pg_df_1.loc[:, 'DOY'][pg_df_1.index == repr(i+1986)].values.astype(np.int32), 
            pg_df_1.loc[:, 'T#AD'][pg_df_1.index == repr(i+1986)].values.astype(np.float64),
            color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    
plt.legend(loc='best', ncol=3)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Tiller number(TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Tiller number(no/ha)', fontsize=15)
#ax.set_ylim(3, 28)
plt.savefig('181204_plant_tiller_number.png', bbox_inches='tight')
plt.show()

#classify THE GRAPH BY ANNUAL YIELD(Leaf Area Index)
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    im = ax.plot(pg_df_1.loc[:, 'DOY'][pg_df_1.index == repr(i+1986)].values.astype(np.int32), 
            pg_df_1.loc[:, 'LAID'][pg_df_1.index == repr(i+1986)].values.astype(np.float64),
            color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    
plt.legend(loc='best', ncol=2)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Leaf Area Index (TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Leaf Area Index(leafarea/unitarea)', fontsize=15)
#ax.set_ylim(3, 28)
plt.savefig('181204_plant_LAI.png', bbox_inches='tight')
plt.show()





        




























