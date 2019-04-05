#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 09:23:10 2019

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



def DATE2DOY(datetime):
    """
    datetime: str
        the format of the datetime is like "yyyy-mm-dd"
        if 'Nan' date is assigned as datetime, this function returns 0.

    return doy: int
    """
    if type(datetime) == float:
        return 0
    else:
        date = datetime[5:]
        year = int(datetime[:4])
        DOY = 0
        if year % 4 == 0:
            if date[:2] == '01':
                DOY = DOY + int(date[3:])
            elif date[:2] == '02':
                DOY = 31 + int(date[3:])
            elif date[:2] == '03':
                DOY = 60 + int(date[3:])
            elif date[:2] == '04':
                DOY = 91 + int(date[3:])
            elif date[:2] == '05':
                DOY = 121 + int(date[3:])
            elif date[:2] == '06':
                DOY = 152 + int(date[3:])
            elif date[:2] == '07':
                DOY = 182 + int(date[3:])
            elif date[:2] == '08':
                DOY = 213 + int(date[3:])
            elif date[:2] == '09':
                DOY = 244 + int(date[3:])
            elif date[:2] == '10':
                DOY = 274 + int(date[3:])
            elif date[:2] == '11':
                DOY = 305 + int(date[3:])
            elif date[:2] == '12':
                DOY = 335 + int(date[3:])

        else:
            if date[:2] == '01':
                DOY = DOY + int(date[3:])
            elif date[:2] == '02':
                DOY = 31 + int(date[3:])
            elif date[:2] == '03':
                DOY = 59 + int(date[3:])
            elif date[:2] == '04':
                DOY = 90 + int(date[3:])
            elif date[:2] == '05':
                DOY = 120 + int(date[3:])
            elif date[:2] == '06':
                DOY = 151 + int(date[3:])
            elif date[:2] == '07':
                DOY = 181 + int(date[3:])
            elif date[:2] == '08':
                DOY = 212 + int(date[3:])
            elif date[:2] == '09':
                DOY = 243 + int(date[3:])
            elif date[:2] == '10':
                DOY = 273 + int(date[3:])
            elif date[:2] == '11':
                DOY = 304 + int(date[3:])
            elif date[:2] == '12':
                DOY = 334 + int(date[3:])

        return DOY
    
    
def DOY2DATE(doy, year=2018):
    """
    doy: int
        the day of the year, 1th January -> 1, 31th December -> 365
    year: int
        the year of targeted year (ex. 2018)

    return datetime: str (ex. 2018-01-01)
    """

    if year%4 == 0:
        if doy >= 1 and doy< 32:
            date = repr(year) + '-01-{0:02d}'.format(doy)
        elif doy >= 32 and doy < 61:
            date = repr(year) + '-02-{0:02d}'.format(doy - 31)
        elif doy >= 61 and doy < 92:
            date = repr(year) + '-03-{0:02d}'.format(doy - 60)
        elif doy >= 92 and doy < 122:
            date = repr(year) + '-04-{0:02d}'.format(doy - 91)
        elif doy >= 122 and doy < 153:
            date = repr(year) + '-05-{0:02d}'.format(doy - 121)
        elif doy >= 153 and doy < 183:
            date = repr(year) + '-06-{0:02d}'.format(doy - 152)
        elif doy >= 183 and doy < 214:
            date = repr(year) + '-07-{0:02d}'.format(doy - 182)
        elif doy >= 214 and doy < 245:
            date = repr(year) + '-08-{0:02d}'.format(doy - 213)
        elif doy >= 245 and doy < 275:
            date = repr(year) + '-09-{0:02d}'.format(doy - 244)
        elif doy >= 275 and doy < 306:
            date = repr(year) + '-10-{0:02d}'.format(doy - 274)
        elif doy >= 306 and doy < 336:
            date = repr(year) + '-11-{0:02d}'.format(doy - 305)
        elif doy >= 336 and doy < 367:
            date = repr(year) + '-12-{0:02d}'.format(doy - 335)

    else:
        if doy >= 1 and doy< 32:
            date = repr(year) + '-01-{0:02d}'.format(doy)
        elif doy >= 32 and doy < 60:
            date = repr(year) + '-02-{0:02d}'.format(doy - 31)
        elif doy >= 60 and doy < 91:
            date = repr(year) + '-03-{0:02d}'.format(doy - 59)
        elif doy >= 91 and doy < 121:
            date = repr(year) + '-04-{0:02d}'.format(doy - 90)
        elif doy >= 121 and doy < 152:
            date = repr(year) + '-05-{0:02d}'.format(doy - 120)
        elif doy >= 152 and doy < 182:
            date = repr(year) + '-06-{0:02d}'.format(doy - 151)
        elif doy >= 182 and doy < 213:
            date = repr(year) + '-07-{0:02d}'.format(doy - 181)
        elif doy >= 213 and doy < 244:
            date = repr(year) + '-08-{0:02d}'.format(doy - 212)
        elif doy >= 244 and doy < 274:
            date = repr(year) + '-09-{0:02d}'.format(doy - 243)
        elif doy >= 274 and doy < 305:
            date = repr(year) + '-10-{0:02d}'.format(doy - 273)
        elif doy >= 305 and doy < 335:
            date = repr(year) + '-11-{0:02d}'.format(doy - 304)
        elif doy >= 335 and doy < 366:
            date = repr(year) + '-12-{0:02d}'.format(doy - 334)

    return date


def datelist2DOY(datelist):
    """
    datelist: list or numpy ndarray
        the list for the date 
        
    return doylist: list
    """
    
    doylist = []
    for i in datelist:
        doy = DATE2DOY(i)
        doylist.append(doy)
    
    return doylist

def doylist2Date(doylist, year=2018):
    datelist = []
    for i in doylist:
        #print(i)
        date = DOY2DATE(i, year=year)
        datelist.append(date)
    
    return datelist

"""
190111 compareing direct-seeding and transplanting scenario for each planting date 
in terms of quantile(0.75) - quantile(0.25)

1. load the summary.OUT file of each simulation from Reiton.py file
2. convert data type from object to np.float32 or np.int32
3. generate quantile df 
4. generate graph for yield(HWAH), flowering date(ADAT), and maturity date(MDAT) 
"""

"""
190111 Read Summary.OUT file of the crop-simulation. (Direct-sowing)
This file contains Yield(HWAH), Anthesis date(ADAT) and Maturity date(MDAT) information.
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
190111 Read Summary.OUT file of the crop-simulation. (Transplanting)
"""
record = []
with open(os.getcwd() + '/2019-01-09T22-14-43-673Ze7e3e8533b0b2927/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])



#1. generate list which consists of summary.OUT df
dflist = [sum_df5, sum_df5T, sum_dfT]

#2. convert type from object to np.int32
newlist = []
for i in range(len(dflist)):
    df = dflist[i].loc[:,["HWAH","ADAT","MDAT"]]
    val = df.values.astype(np.int32)
    df_n = pd.DataFrame(val, index=df.index, columns=df.columns)
    newlist.append(df_n)
    print(i)
"""
190122 less residue pattern checking.
"""
record = []
with open(os.getcwd() + '/2019-01-17T02-04-32-234Z77415c7a5696a6ea/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum_dfT = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])    



"""
#3. generate cumulative histogram of each item(HWAH, MDAT, ADAT)
"""
"""
#YIELD(HWAH), direct-sowing
"""
order=newlist[0].sort_values("HWAH").index
ord_df = pd.DataFrame(np.arange(1,101), index=order, columns=['ORDER'])
sum_ds = pd.concat([newlist[0], ord_df], axis=1, sort=True)

val = newlist[0]['HWAH'].values

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

yy1 = newlist[0].loc[order[50],'HWAH']*0.7
yy2 = newlist[0].loc[order[50],'HWAH']*0.2
Ind = np.abs(val - yy1).argmin()+1 

ax.hist(val, bins=50, cumulative=True, color='red', histtype="barstacked")
ax.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[0].loc[order[20],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[0].loc[order[50],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[0].loc[order[80],'HWAH'])+"kg/ha")
ax.plot([yy1, yy1],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds.loc[repr(Ind),"ORDER"])+"%")


plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Yield(Direct-sowing)", fontsize=18)
ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Yield_ds_pdate194.png", bbox_inches='tight')
plt.show()

"""
#transplanting
"""
order=newlist[1].sort_values("HWAH").index
ord_df = pd.DataFrame(np.arange(1,101), index=order, columns=['ORDER'])
sum_ds = pd.concat([newlist[1], ord_df], axis=1, sort=True)

val = newlist[1]['HWAH'].values

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

yy1 = newlist[1].loc[order[50],'HWAH']*0.7
yy2 = newlist[1].loc[order[50],'HWAH']*0.2
Ind = np.abs(val - yy1).argmin()+1 

ax.hist(newlist[1]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[1].loc[order[20],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[1].loc[order[50],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[1].loc[order[80],'HWAH'])+"kg/ha")
ax.plot([yy1, yy1],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds.loc[repr(Ind),"ORDER"])+"%")


plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Yield(transplanting)", fontsize=18)
ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Yield_tp_pdate214.png", bbox_inches='tight')

plt.show()


#compare both
order0 = newlist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([newlist[0], ord_df0], axis=1, sort=True)
order1 = newlist[1].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([newlist[1], ord_df1], axis=1, sort=True)

val0 = newlist[0]['HWAH'].values
val1 = newlist[1]['HWAH'].values

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

yy1_0 = newlist[0].loc[order0[50],'HWAH']*0.7
yy2_0 = newlist[0].loc[order0[50],'HWAH']*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - 2000).argmin()+1 
yy1_1 = newlist[1].loc[order1[50],'HWAH']*0.7
yy2_1 = newlist[1].loc[order1[50],'HWAH']*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - 2000).argmin()+1 

ax.hist(newlist[0]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[1].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[1].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[1].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([2000, 2000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(newlist[1]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[1].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[1].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[1].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([2000, 2000],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
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

"""
190113 organic template(transplant)
"""
order=newlist[2].sort_values("HWAH").index
ord_df = pd.DataFrame(np.arange(1,101), index=order, columns=['ORDER'])
sum_ds = pd.concat([newlist[2], ord_df], axis=1, sort=True)

val = newlist[2]['HWAH'].values

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

yy1 = newlist[2].loc[order[50],'HWAH']*0.7
yy2 = newlist[2].loc[order[50],'HWAH']*0.2
Ind = np.abs(val - yy1).argmin()+1 

ax.hist(newlist[2]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([500, 3000],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[2].loc[order[20],'HWAH'])+"kg/ha")
ax.plot([500, 3000],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[2].loc[order[50],'HWAH'])+"kg/ha")
ax.plot([500, 3000],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[2].loc[order[80],'HWAH'])+"kg/ha")
ax.plot([yy1, yy1],[0,100], color="green", label="The Risk of 30% Lower than Median = "+repr(sum_ds.loc[repr(Ind),"ORDER"])+"%")


plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Yield(transplanting)", fontsize=18)
ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190114_CDF_Reiton_Yield_tp_pdate214_temp.png", bbox_inches='tight')

plt.show()


"""
#ANTHESIS DATE(ADAT), direct-sowing pattern
"""
order=newlist[0].sort_values("ADAT").index

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

#date format is "yyyydoy", then convert to doy from 2018-01-01.
adat = []
for i in range(100):
    if newlist[0]['ADAT'][i] < 2019000:
        val = newlist[0]['ADAT'][i] - 2018000
    else:
        val = newlist[0]['ADAT'][i] - 2019000+365
    adat.append(val)


ax.hist(np.asarray(adat), bins=85, cumulative=False, color='red', histtype="barstacked")
#ax.plot([280, 375],[20, 20], color="black", 
#        label="20 percentile ADAT="+DOY2DATE(newlist[0].loc[order[20],'ADAT']-2018000))
#ax.plot([280, 375],[50, 50], color="blue", 
#        label="50 percentile ADAT="+DOY2DATE(newlist[0].loc[order[50],'ADAT']-2018000))
#ax.plot([280, 375],[80, 80], color="orange", 
#        label="80 percentile ADAT="+DOY2DATE(newlist[0].loc[order[80],'ADAT']-2018000))

#plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax.set_xlabel("The anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.xticks(np.arange(280, 390, 10), 
           np.concatenate((doylist2Date(np.arange(280, 365, 10)), 
                           doylist2Date(np.arange(5, 25, 10),year=2019))))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190114_CDF_Reiton_Anthesis_ds_pdate194_hist.png", bbox_inches='tight')
plt.show()

"""
#transplanting pattern
"""
order=newlist[1].sort_values("ADAT").index

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

adat = []
for i in range(100):
    if newlist[1]['ADAT'][i] < 2019000:
        val = newlist[1]['ADAT'][i] - 2018000
    else:
        val = newlist[1]['ADAT'][i] - 2019000+365
    adat.append(val)
adat.sort()

ax.hist(np.asarray(adat[:99]), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([280, 375],[20, 20], color="black", 
        label="20 percentile ADAT="+DOY2DATE(newlist[1].loc[order[20],'ADAT']-2018000))
ax.plot([280, 375],[50, 50], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(newlist[1].loc[order[50],'ADAT']-2018000))
ax.plot([280, 375],[80, 80], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(newlist[1].loc[order[80],'ADAT']-2018000))

plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Anthesis date(Transplanting)", fontsize=18)
ax.set_xlabel("The anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.xticks(np.arange(280, 380, 10), 
           np.concatenate((doylist2Date(np.arange(280, 365, 10)), 
                           doylist2Date(np.arange(5, 15, 10),year=2019))))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Anthesis_tp_pdate214.png", bbox_inches='tight')

plt.show()

"""
#MATURITY DATE, direct-sowing pattern
"""
order=newlist[0].sort_values("MDAT").index

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

adat = []
for i in range(100):
    if newlist[0]['MDAT'][i] < 2019000:
        val = newlist[0]['MDAT'][i] - 2018000
    else:
        val = newlist[0]['MDAT'][i] - 2019000+365
    adat.append(val)


ax.hist(np.asarray(adat), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([310, 410],[20, 20], color="black", 
        label="20 percentile MDAT="+DOY2DATE(newlist[0].loc[order[20],'MDAT']-2018000))
ax.plot([310, 410],[50, 50], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(newlist[0].loc[order[50],'MDAT']-2018000))
ax.plot([310, 410],[80, 80], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(newlist[0].loc[order[80],'MDAT']-2018000))

plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.xticks(np.arange(310, 420, 10), 
           np.concatenate((doylist2Date(np.arange(310, 365, 10)), 
                           doylist2Date(np.arange(5, 55, 10),year=2019))))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Maturity_ds_pdate194.png", bbox_inches='tight')
plt.show()


"""
#transplanting pattern
"""
order=newlist[1].sort_values("MDAT").index

fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

adat = []
for i in range(100):
    if newlist[1]['MDAT'][i] < 2019000:
        val = newlist[1]['MDAT'][i] - 2018000
    else:
        val = newlist[1]['MDAT'][i] - 2019000+365
    adat.append(val)
adat.sort()

ax.hist(np.asarray(adat[:99]), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([310, 410],[20, 20], color="black", 
        label="20 percentile MDAT="+DOY2DATE(newlist[1].loc[order[20],'MDAT']-2018000))
ax.plot([310, 410],[50, 50], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(newlist[1].loc[order[50],'MDAT']-2018000))
ax.plot([310, 410],[80, 80], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(newlist[1].loc[order[80],'MDAT']-2018000))

plt.legend(loc="best", fontsize=14)
ax.set_title("The Cumulative Histogram of Maturity date(Transplanting)", fontsize=18)
ax.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
plt.xticks(np.arange(310, 410, 10), 
           np.concatenate((doylist2Date(np.arange(310, 365, 10)), 
                           doylist2Date(np.arange(5, 45, 10),year=2019))))
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190108_Reiton_RIX_png/190111_CDF_Reiton_Maturity_tp_pdate214.png", bbox_inches='tight')
plt.show()



"""
"""
order0 = newlist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,101), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([newlist[0], ord_df0], axis=1, sort=True)
order1 = newlist[1].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,101), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([newlist[1], ord_df1], axis=1, sort=True)

val0 = newlist[0]['HWAH'].values
val1 = newlist[1]['HWAH'].values

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2)

yy1_0 = newlist[0].loc[order0[50],'HWAH']*0.7
yy2_0 = newlist[0].loc[order0[50],'HWAH']*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - 2500).argmin()+1 
yy1_1 = newlist[1].loc[order1[50],'HWAH']*0.7
yy2_1 = newlist[1].loc[order1[50],'HWAH']*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - 2500).argmin()+1 

ax.hist(newlist[0]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[0].loc[order0[20],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[0].loc[order0[50],'HWAH'])+"kg/ha")
ax.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[0].loc[order0[80],'HWAH'])+"kg/ha")
ax.plot([2500, 2500],[0,100], color="green", label="The Risk of Lower than 2500kg/ha = "+repr(sum_ds0.loc[repr(Ind0),"ORDER"])+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(newlist[1]['HWAH'].values, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([1000, 4300],[20, 20], color="black", label="20 percentile Yield="+repr(newlist[1].loc[order1[20],'HWAH'])+"kg/ha")
ax2.plot([1000, 4300],[50, 50], color="blue", label="50 percentile Yield="+repr(newlist[1].loc[order1[50],'HWAH'])+"kg/ha")
ax2.plot([1000, 4300],[80, 80], color="orange", label="80 percentile Yield="+repr(newlist[1].loc[order1[80],'HWAH'])+"kg/ha")
ax2.plot([2500, 2500],[0,100], color="green", label="The Risk of Lower than 2500kg/ha = "+repr(sum_ds1.loc[repr(Ind1),"ORDER"])+"%")
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
plt.savefig("190108_Reiton_RIX_png/190124_CDF_Reiton_Yield_TP_VS_DS2.png", bbox_inches='tight')

plt.show()        
        
        
        
        
        
        
        
