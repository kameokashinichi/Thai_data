#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 12:49:44 2018

@author: kameokashinichi
"""

#181205 convert WTD into DataFrame

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import shutil
from pylab import cm
from statistics import mean, stdev, median
from sklearn import linear_model

sskt = WTD2DataFrame('SSKT.WTD')

#classify by solar radiation
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'SRAD'], 
    color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    #print(i)
    
plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Solar Radiation (TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Solar Radiation (MJ/m2)', fontsize=15)
ax.set_xlim(210, 240)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()

hwah = [2626, 1405, 1978, 1798, 2168, 1907, 1605, 2268, 1904,
        644, 1544, 586, 1429, 1853, 1556, 879, 1681, 1809, 604, 
        1386, 1561, 2252, 2422, 1546, 748, 1928, 1815, 1893, 614, 633, 2290, 640]


re.search('^86', sskt.index[0])

#classify the rainfall
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'RAIN'], 
    color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    #print(i)
    
plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Rain Fall (TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Rain Fall (mm)', fontsize=15)
ax.set_xlim(200, 220)
ax.set_ylim(0, 150)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()


#max temperature
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'TMAX'], 
    color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    #print(i)
    
plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Max temperature (TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Tmax (cel)', fontsize=15)
ax.set_xlim(215, 225)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()


#min temperature
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

n = 0
for i in range(0, 32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ax.plot(np.arange(1, len(df.index)+1), df.loc[:, 'TMAX'], 
    color=cm.RdBu(hwah[i]/2626), label=repr(1986+i)+'(y='+repr(hwah[i])+')')
    #print(i)
    
plt.legend(loc='best', ncol=5)
#plt.xticks(np.arange(len(wthdf.index)), np.inspace(1, 365, num=5))
plt.title("Min temperature (TPDOY=213)", fontsize=18)
plt.xlabel('Day of year', fontsize=15)
plt.ylabel('Tmin (cel)', fontsize=15)
ax.set_xlim(215, 225)
#plt.savefig('181204_soil_N_yield.png', bbox_inches='tight')
plt.show()


#calculate average solar radiation.
ave = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ave.append(mean(df.iloc[200:230, 0]))
    
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)
ax2 = ax.twinx()

ax.bar(np.arange(0, 32), ave, width=0.4, label="SRAD(MJ/m2)", color="blue")
ax.legend(bbox_to_anchor = (0.8, 1.0))
ax2.bar(np.arange(0, 32)+0.4, hwah, width=0.4, label="yield(kg/ha)", color="red")

plt.legend(loc = 'best')
plt.title("Mean Solar Radiation")
plt.xlabel('Year')
ax.set_ylabel('SRAD(MJ/m2)')
ax2.set_ylabel('Yield(kg/ha)')
plt.xticks(np.arange(0, 32, 3), np.arange(1986, 2018, 3))


plt.show()

#scatter plot of the relation between rainfall and yield

rain = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    rain.append(sum(df.iloc[200:215, 3]))

#prepare linear regression formula
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X = np.asarray(rain).reshape(-1, 1)
Y = np.asarray(hwah).reshape(-1, 1)

clf.fit(X, Y)

ax.scatter(rain, hwah, s=20, c='red')
ax.plot(X, clf.predict(X), color = 'blue',  label='R2 value={:.3f}'.format(clf.score(X,Y)))

plt.legend(loc='best', fontsize=15)
plt.title("Rainfall amount VS Yield", fontsize=18)
plt.xlabel('Rain fall amount from DOY200-215 (mm)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181205_rainfall_amount_VS_yield.png')

plt.show()


#solar radiation VS yield
ave = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    ave.append(mean(df.iloc[200:230, 0]))

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X2 = np.asarray(ave).reshape(-1, 1)
Y2 = np.asarray(hwah).reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(ave, hwah, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue',  label='coef={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Average SRAD VS Yield", fontsize=18)
plt.xlabel('Average Solar Radiation during DOY200-230 (MJ/m2)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181205_solar_radiation_VS_yield.png')

plt.show()

#Tmax VS yield
Tmax_ave = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    Tmax_ave.append(mean(df.iloc[200:230, 1]))

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X2 = np.asarray(Tmax_ave).reshape(-1, 1)
Y2 = np.asarray(hwah).reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(Tmax_ave, hwah, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Average Tmax VS Yield", fontsize=18)
plt.xlabel('Average Tmax during DOY200-230 (cel)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181205_Tmax_VS_yield.png')

plt.show()

#Tmin vs yield
Tmin_ave = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    Tmin_ave.append(mean(df.iloc[200:230, 2]))

fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X2 = np.asarray(Tmin_ave).reshape(-1, 1)
Y2 = np.asarray(hwah).reshape(-1, 1)

clf.fit(X2, Y2)

ax.scatter(Tmin_ave, hwah, s=20, c='red')
ax.plot(X2, clf.predict(X2), color = 'blue', label='R2={:.3f}'.format(clf.score(X2,Y2)))

plt.legend(loc='best', fontsize=15)
plt.title("Average Tmin VS Yield", fontsize=18)
plt.xlabel('Average Tmin during DOY200-230 (cel)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181205_Tmin_VS_yield.png')

plt.show()

#whole season rainy vs yield
rain = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    rain.append(sum(df.iloc[200:330, 3]))

#prepare linear regression formula
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X = np.asarray(rain).reshape(-1, 1)
Y = np.asarray(hwah).reshape(-1, 1)

clf.fit(X, Y)

ax.scatter(rain, hwah, s=20, c='red')
ax.plot(X, clf.predict(X), color = 'blue',  label='R2 value={:.3f}'.format(clf.score(X,Y)))

plt.legend(loc='best', fontsize=15)
plt.title("Rainfall amount VS Yield", fontsize=18)
plt.xlabel('Rain fall amount from DOY200-215 (mm)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181205_rainfall_amount_VS_yield_ver2.png')

plt.show()

#rainy in the juvenile phase vs yield
rain = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    rain.append(sum(df.iloc[213:250, 3]))

#prepare linear regression formula
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X = np.asarray(rain).reshape(-1, 1)
Y = np.asarray(hwah).reshape(-1, 1)

clf.fit(X, Y)

ax.scatter(rain, hwah, s=20, c='red')
ax.plot(X, clf.predict(X), color = 'blue',  label='R2 value={:.3f}'.format(clf.score(X,Y)))

plt.legend(loc='best', fontsize=15)
plt.title("Rainfall amount VS Yield", fontsize=18)
plt.xlabel('Rain fall amount from DOY213-250 (mm)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181206_rainfall_amount_VS_yield_ver2.png')

plt.show()

#rainy in the maturity phase vs yield
rain = []
for i in range(0,32):
    num = repr(i+86)
    if len(num) == 3:
        num = num[1:]
    df = searchElementforX(sskt, '^'+num)
    rain.append(sum(df.iloc[290:330, 3]))

#prepare linear regression formula
fig = plt.figure(figsize = (11, 8))
ax = fig.add_subplot(1,1,1)

clf = linear_model.LinearRegression()
X = np.asarray(rain).reshape(-1, 1)
Y = np.asarray(hwah).reshape(-1, 1)

clf.fit(X, Y)

ax.scatter(rain, hwah, s=20, c='red')
ax.plot(X, clf.predict(X), color = 'blue',  label='R2 value={:.3f}'.format(clf.score(X,Y)))

plt.legend(loc='best', fontsize=15)
plt.title("Rainfall amount VS Yield", fontsize=18)
plt.xlabel('Rain fall amount from DOY290-330 (mm)', fontsize=16)
plt.ylabel("Final Yield(kg/ha)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=15, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, visible=True)
plt.savefig('181206_rainfall_maturity_VS_yield_ver2.png')

plt.show()


