#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan  8 14:33:39 2019

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
http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/cropsim/exec/2019-01-08T05-28-14-772Z65deb2087a92ce23
soilid -> "JP_NRPH10F"
planting method -> Direct-sowing
Planting date -> 18194

soilWat.OUT, Summary.OUT, SoilNi.OUT, PlantN.OUT, 100 weather scenarios
"""
"""
190108 read water stress Dssat file.(SoilWat.OUT)
"""

soilW = []
with open(os.getcwd() + '/2019-01-08T05-28-14-772Z65deb2087a92ce23/SoilWat.OUT', 'r') as f:
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
    elif len(stress[i]) != 22:
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
    
sw_df5 = pd.DataFrame(s_stress[:, 1:], columns=columns[1:], index = newcol)
 
"""
190108 Summary.OUT
"""
record = []
with open(os.getcwd() + '/2019-01-08T05-28-14-772Z65deb2087a92ce23/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df5 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

"""
190108 SoilNi.OUT read Soil N Dssat file.
"""
soilN = []
with open(os.getcwd() + '/2019-01-08T05-28-14-772Z65deb2087a92ce23/SoilNi.OUT', 'r') as f:
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
    elif len(stressN[i]) != 30:
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
190108 PlantN.OUT plant N flow
"""

#read Soil N Dssat file.
PN = []
with open(os.getcwd() + '/2019-01-08T05-28-14-772Z65deb2087a92ce23/PlantN.OUT', 'r') as f:
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
190108 PlantGro.OUT degree days etc.
"""

PG = []
with open(os.getcwd() + '/2019-01-08T05-28-14-772Z65deb2087a92ce23/PlantGro.OUT', 'r') as f:
    for row in f:
        PG.append(row.strip())
        
PG = PG[13:]

stress = []     
for row in PG:
    element = row.split()
    stress.append(element)   
        
columns = stress[0]

#extract available rows
stress = np.asarray(stress)
num = []
for i in range(len(stress)):
    if len(stress[i]) == 36 and stress[i][0] == '2018':
        num.append(i)
    else:
        pass

pg = stress[num]

"""
for i in range(len(sw)):
    if len(sw[i]) != 21:
        print(i)
"""

#convert list to np.array    
pg_stress = []
for i in range(len(pg)):
    pg_stress.append(pg[i])
pg_stress = np.asarray(pg_stress)    

pg_df = pd.DataFrame(pg_stress[:, 1:], columns=columns[1:], index = pg_stress[:,0]) 

#change the index from year to simulation number
number = [0]
for i in range(len(pg_df.index)):
    if i == len(pg_df.index)-1:
        break
    elif int(pg_df.iloc[i, 0]) > int(pg_df.iloc[i+1, 0]):
        number.append(i+1)

#convert np.ndarray to pd.DataFrame(index is the number of experiment)
newcol = np.array([])
for j in range(len(number)):
    if j == 99:
        a = np.repeat(j+1, len(pg_df.index)-number[j])
        newcol = np.append(newcol, a)
    else:
        a = np.repeat(j+1, number[j+1]-number[j])
        newcol = np.append(newcol, a)
    
pg_df5 = pd.DataFrame(pg_stress[:, 1:].astype(np.float32), columns=columns[1:], index = newcol)



"""
190108 analyze the relation between yield(HWAH) and surface NO3(NI1D)
"""
info = sum_df5.loc[:, ["HDAT","HWAH", "PRCP"]].values.astype(np.float32)
sum_df5_1 = pd.DataFrame(info, index=sum_df5.index, columns=["HDAT","HWAH", "PRCP"])

order1 = sum_df5_1.sort_values("HWAH")["HWAH"].index

juv_no1 = sn_df5[sn_df5["DOY"]=="225"]
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
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)   #sum_df1.sort_values("HWAH")

clf = linear_model.LinearRegression()
X2 = no3.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(no3, hwah4, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("NO3 in soil at seedling stage(DAS61) VS Yield", fontsize=18)
plt.xlabel('NO3 content in surface layer (ppm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('190108_Reiton_RIX_png/190108_NH4_surface_in_DAS61_VS_yield_HC_GEN0005.png')

plt.show()

#check the order of NO3 concentration and yield
info = juv_no1.loc[:,["NI1D","NI2D","NH1D","NH2D"]].values.astype(np.float32)
juv_no1_1 = pd.DataFrame(info, index=juv_no1.index, columns=["NI1D","NI2D","NH1D","NH2D"])

for i in range(100):
    print(juv_no1_1.sort_values("NI1D").index[i],
          sum_df3.loc[repr(int(juv_no1_1.sort_values("NI1D").index[i])),"HWAH"])

#visualize single year's N movement (9,23,91,7,53,14 is outlayer)
fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

#wnum = int(order1[90])
wnum = 68

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
plant.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha)", fontsize=15)
ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+sum_df5.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()


"""
190108 check the degree-day VS yield of each scenario
"""

dttd = []
for i in range(100):
    df = pg_df5[pg_df5.index == i+1]
    dd = sum(pg_df5[pg_df5.index == i+1].query("200<DOY<320")["DTTD"].values)
    dttd.append(dd)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

dttd = np.asarray(dttd)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = dttd.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(dttd, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),dttd,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Degree-Days during DOY 195-305 VS Yield", fontsize=18)
plt.xlabel('Degree-Days during DOY 195-305 (average-celcius*day)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()

#forcus on particular growth stage
dttd2 = []
for i in range(100):
    df = pg_df5[pg_df5.index == i+1]
    if np.shape(df[df["GSTD"]==2])[0] != 0:
        gs = df[df["GSTD"]==2]
        dd = sum(gs["DTTD"].values)
    else:
        dd = 0
    dttd2.append(dd)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

dttd2 = np.asarray(dttd2)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = dttd2.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(dttd2, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),dttd2,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Degree-Days during growth stage 2 VS Yield", fontsize=18)
plt.xlabel('Degree-Days during growth stage 2 (average-celcius*day)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#ax.set_xlim(-10, 200)
#plt.savefig('181224_Dssat_png/181226_Precipitation_DAS60_70_VS_Yield_SSKT8605.png', bbox_inches='tight')

plt.show()


#190108 Degree-days vs precipitation during cultivation
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

dttd = np.asarray(dttd)
prcpA = sum_df5.loc[:, 'PRCP'].values.astype(np.float32)

clf = linear_model.LinearRegression()
X2 = dttd.reshape(-1, 1)
Y2 = prcpA.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(dttd, prcpA, s=40, c=sum_df5.loc[:, 'HWAH'].values.astype(np.float32), cmap=cm.Reds)

for a, b, c in zip(np.arange(1,101),dttd,prcpA):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Degree-Days during DOY 215-320 VS Precipitation during cultivation", fontsize=18)
plt.xlabel('Degree-Days during DOY 215-320 (average-celcius*day)', fontsize=16)
plt.ylabel("Precipitation amount(mm)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)

plt.savefig('190108_Reiton_RIX_png/190110_Degree-days_DOY215_320_VS_Precipitation_JP_NRPH10F.png', bbox_inches='tight')

plt.show()

"""
190108 soil water content(SW1D cm3/cm3) VS yield
"""

order1 = sum_df5_1.sort_values("HWAH")["HWAH"].index

fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

for i in range(7):
    wnum = int(order1[i])
    swtd = sw_df5.loc[:, 'SWTD'][sw_df5.index == wnum].values.astype(np.float32)
    doy = sw_df5.loc[:, 'DOY'][sw_df5.index == wnum].values.astype(np.int32)
    ax.plot(doy, swtd, color = 'blue')
for i in range(93,100):
    wnum = int(order1[i])
    swtd = sw_df5.loc[:, 'SWTD'][sw_df5.index == wnum].values.astype(np.float32)
    doy = sw_df5.loc[:, 'DOY'][sw_df5.index == wnum].values.astype(np.int32)
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
ax.set_xlim(180, 260)
#ax.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
#plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('181224_Dssat_png/190105_N_flow_in_1993_SSKT9605.png', bbox_inches='tight')
plt.show()

"""
190108 check the correlation between SWTD(Total soil water) and HWAH
"""

doy = sw_df5.loc[:, 'DOY'].values.astype(np.int32).reshape(-1, 1)
sw2d = sw_df5.loc[:,['SW1D', 'SW2D', 'SWTD']].values.astype(np.float32)
swdoy = np.concatenate((doy,sw2d), axis=1)
swdoy_df = pd.DataFrame(swdoy, index=sw_df5.index, columns=["DOY", 'SW1D', 'SW2D',"SWTD"])
wc = []
for i in range(1, 101):
    df = swdoy_df[sw_df5.index == i]
    ave = mean(df.query("290 < DOY <300")["SWTD"])
    wc.append(ave)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(wc)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),prcp4,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Soil total water in DOY290-300 VS Yield", fontsize=18)
plt.xlabel('Soil total water in DOY290-300 (mm)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('190108_Reiton_RIX_png/190108_soil_total_water_DOY190_200_VS_Yield_JP_NRPH10F.png', bbox_inches='tight')

plt.show()

#relationship between stress during DOY280-300(STWD<280) vs yield
sday = []
for i in range(1,101):
    df = swdoy_df[swdoy_df.index == i].query("280<DOY<300")
    n = 0
    for j in range(len(df.index)):
        if df.iloc[j, 3] < 280:
            n = n+1
    
    sday.append(n)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(sday)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),prcp4,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Total water stressful days DOY280-300 VS Yield", fontsize=18)
plt.xlabel('Water stress day SWTD<280 (number)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('190108_Reiton_RIX_png/190108_soil_total_water_DOY280_300_SWTD<280_VS_Yield_JP_NRPH10F.png', bbox_inches='tight')

plt.show()

#relationship between stress during DOY195-210(STWD<200) vs yield
#if the stress is loaded in this season, the growth starting date is delay 20 days
sday2 = []
for i in range(1,101):
    df = swdoy_df[swdoy_df.index == i].query("199<DOY<210")
    n = 0
    for j in range(len(df.index)):
        if df.iloc[j, 3] < 220:
            n = n+1
    
    sday2.append(n)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(sday2)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),prcp4,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Total water stressful days DOY200_210 VS Yield", fontsize=18)
plt.xlabel('Water stress day SWTD<220 (number)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
#plt.savefig('190108_Reiton_RIX_png/190108_soil_total_water_DOY200_210_SWTD<220_VS_Yield_JP_NRPH10F.png', bbox_inches='tight')

plt.show()

#relationship between stress days and yield
sday3 = np.asarray(sday)+np.asarray(sday2)

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

prcp4 = np.asarray(sday3)
hwah4 = sum_df5.loc[:, 'HWAH'].values.astype(np.int32)

clf = linear_model.LinearRegression()
X2 = prcp4.reshape(-1, 1)
Y2 = hwah4.reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(prcp4, hwah4, s=20, c='red')

for a, b, c in zip(np.arange(1,101),prcp4,hwah4):
    ax.annotate(a, xy=(b,c),size=11)
    
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Total water stressful days VS Yield", fontsize=18)
plt.xlabel('Water stress day (DOY200-210, DOY280-300)', fontsize=16)
plt.ylabel("Final Yield (kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
ax.set_xlim(-1, 3)
ax.set_ylim(3300,3700)
plt.savefig('190108_Reiton_RIX_png/190108_soil_total_water_stress_VS_Yield_JP_NRPH10F_High_yield.png', bbox_inches='tight')

plt.show()



"""
190108 Relationship among rain, soil water(SW1D,SW2D,SW3D) and soilN(NI1D,NH1D).
-> If there is water stress either during DOY195-205 or DOY290-300, 
the yield might be reduced
"""
order1 = sum_df5_1.sort_values("HWAH")["HWAH"].index

fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

#wnum = int(order1T[99])
wnum = 43

dfw = sw_df5[sn_df5.index == wnum]
dfs = sn_df5[sn_df5.index == wnum]
dfp = pn_df5[pn_df5.index == wnum]
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
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+sum_df5.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
#ax2.set_ylim(0, 1)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190108_N_and_water_flow_JP_NRPH10F.png', bbox_inches='tight')
plt.show()


#In case of SW1D
order1 = sum_df5_1.sort_values("HWAH")["HWAH"].index

fig = plt.figure(figsize = (10, 5))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

#wnum = int(order1[99])
wnum = 24

dfw = sw_df5[sn_df5.index == wnum]
dfs = sn_df5[sn_df5.index == wnum]
dfp = pn_df5[pn_df5.index == wnum]
prep = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
ax.plot(dfs.loc[:, 'DOY'].values.astype(np.int32), 
        dfs.loc[:, 'NI1D'].values.astype(np.float64), 
        color='brown')
ax2.plot(dfw.loc[:, 'DOY'].values.astype(np.int32), 
        dfw.loc[:, 'SW2D'].values.astype(np.float64),
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

plt.legend((no, sw, top, grain, rain), ('soil NO3', 'soil 2nd WC', 'top', 'grain', 'rain'),
           loc="best", fontsize=14)

no.set_visible(False)
sw.set_visible(False)
top.set_visible(False)
grain.set_visible(False)
rain.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("nitrogen contents in soil(kg/ha), daily rainfall(mm)", fontsize=15)
ax2.set_ylabel('Soil water content(cm3/cm3)', fontsize=15)
plt.title("N stream between soil and plant in No" + repr(wnum)+"(yield="+sum_df5.loc[repr(wnum),"HWAH"]+"kg/ha)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(180, 320)
ax2.set_ylim(0, 0.8)
plt.setp(ax.get_xticklabels(), fontsize=13, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=13, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=13, visible=True)
#ax.set_ylim(0, 30)
#plt.savefig('190108_Reiton_RIX_png/190108_N_and_water_flow_JP_NRPH10F.png', bbox_inches='tight')
plt.show()

"""
190108 compare weather between high and low yield scenario
"""

order1 = sum_df5_1.sort_values("HWAH")["HWAH"].index

fig = plt.figure(figsize = (14, 7))
ax = fig.add_subplot(1,1,1)
#ax2 = ax.twinx()

for i in range(5):
    wnum = int(order1[i])
    weath = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
    ax.plot(np.arange(1, len(weath)+1, 1), weath, color = 'blue')
for i in range(95,100):
    wnum = int(order1[i])
    weath = searchElementforX(wlis[wnum-1], '^18')["RAIN"].values
    ax.plot(np.arange(1, len(weath)+1, 1), weath, color = 'red')
   

low, = plt.plot((1,2), (2,2), color="blue", linewidth=10)
high, = plt.plot((1,2), (2,2), color="red", linewidth=10)

plt.legend((low, high), ('Low Yield', "High Yield"),
           loc="best", fontsize=14)

low.set_visible(False)
high.set_visible(False)

#plt.xticks(np.linspace(0, len(nitro_df.index), num=31), np.unique(nitro_df.index))
ax.set_ylabel("Daily Precipitation(mm)", fontsize=15)
#ax2.set_ylabel('daily rainfall(mm)', fontsize=15)
plt.title("Daily Precipitation between high and low yield scenario", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
ax.set_xlim(230, 330)
#ax.set_ylim(0, 1)
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












"""
190108 generate PCA by SWTD
"""








