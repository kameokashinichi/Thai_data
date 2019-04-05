#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 18 11:23:37 2019

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

"""
190118 check te sensitivity of soil water content and icres to final yield
Soil water content is around 0.25, icres is 100 and icren is 0.8 -> 
"2019-01-05T08-02-58-215Z9de7b566152a6862" -> sum1
Soil water content is around 0.15, icres is 100 and icren is 0.8 -> 
"2019-01-06T07-47-24-188Z8573a054be616ec4" -> sum2
Soil water content is around 0.15, icres is 1000 and icren is 2.8 ->
"2019-01-06T08-25-02-155Zab9109340a3fe22a" -> sum3
Soil water content is around 0.05, icres is 1000, icren is 2.8 icrt=500, icnd=300 ->
"2019-01-06T08-32-57-570Zbe428b86db3fbfdf" -> sum4
Almost same as sum4, except icdat(ICDAT=18187) ->
"2019-01-06T08-57-35-111Z1ba740f40d8d26e6" -> sum5

soil ID -> WI_GLTH008
ICDAT -> 18149
PDATE -> 18194
Initial soil condition
@C  ICBL  SH2O  SNH4  SNO3
 1     5   .05  6.50 47.14
 1    15   .07  2.57  4.66
 1    30   .05  0.04  3.88
 1    42   .04  0.07  3.71
 1    55   .04  0.03  1.37
 1    67   .05  0.01  0.98
 1    80   .07  0.01  1.06
 1   100   .05  0.01  1.23
"""
#sum1
record = []
with open(os.getcwd() + '/2019-01-05T08-02-58-215Z9de7b566152a6862/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum1 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum2
record = []
with open(os.getcwd() + '/2019-01-06T07-47-24-188Z8573a054be616ec4/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum2 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum3
record = []
with open(os.getcwd() + '/2019-01-06T08-25-02-155Zab9109340a3fe22a/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum3 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])


#sum4
record = []
with open(os.getcwd() + '/2019-01-06T08-32-57-570Zbe428b86db3fbfdf/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum4 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum5
record = []
with open(os.getcwd() + '/2019-01-06T08-57-35-111Z1ba740f40d8d26e6/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum5 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])


"""
190118 compare the yield by plot
"""

y_value = pd.concat([sum1["HWAH"], sum2["HWAH"], sum3["HWAH"], sum4["HWAH"], sum5["HWAH"]], axis=1).values.astype(np.int32)
y_df = pd.DataFrame(y_value, index=sum1.index, columns=["sum1", "sum2", "sum3", "sum4", "sum5"])

fig = plt.figure(figsize=(12, 6))
ax = fig.add_subplot(1,1,1)

for i in range(len(y_df.columns)):
    ax.plot(np.arange(1, len(y_df.index)+1), y_df.iloc[:, i], 
            color=cm.hsv(i/len(y_df.columns)))
    
sum_1, = plt.plot((1,1),(1,1), color=cm.hsv(0/len(y_df.columns)), linewidth=10)
sum_2, = plt.plot((1,1),(1,1), color=cm.hsv(1/len(y_df.columns)), linewidth=10)
sum_3, = plt.plot((1,1),(1,1), color=cm.hsv(2/len(y_df.columns)), linewidth=10)
sum_4, = plt.plot((1,1),(1,1), color=cm.hsv(3/len(y_df.columns)), linewidth=10)
sum_5, = plt.plot((1,1),(1,1), color=cm.hsv(4/len(y_df.columns)), linewidth=10)

plt.legend((sum_1, sum_2, sum_3, sum_4, sum_5),
           ("high SWC(25%) ("+repr(mean(y_df.iloc[:, 0]))+"kg/ha)", 
            "low SWC(15%)("+repr(mean(y_df.iloc[:, 1]))+"kg/ha)",
            "high Residue(1000kg/ha)("+repr(mean(y_df.iloc[:, 2]))+"kg/ha)", 
            "high Residue with Root ("+repr(mean(y_df.iloc[:, 3]))+"kg/ha)", 
            "DIfferent ICDAT ("+repr(mean(y_df.iloc[:, 4]))+"kg/ha)"), 
           fontsize=14, loc="best")

sum_1.set_visible(False)
sum_2.set_visible(False)
sum_3.set_visible(False)
sum_4.set_visible(False)
sum_5.set_visible(False)

plt.title("Sensitivity of Soil Wate Content and Residue", fontsize=17)
plt.xlabel("Sample ID", fontsize=15)
plt.ylabel("Final yield(kg/ha)", fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
ax.set_xlim(20, 40)

plt.show()


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
#sum1
record = []
with open(os.getcwd() + '/2019-01-25T09-32-55-312Z659a00f91b5791cc/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum1 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum2
record = []
with open(os.getcwd() + '/2019-01-25T09-38-16-204Z51340cc5356b47cc/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum2 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum3
record = []
with open(os.getcwd() + '/2019-01-25T09-41-26-888Z4684f999972c214f/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum3 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum4
record = []
with open(os.getcwd() + '/2019-01-25T09-44-12-143Zb07b705502e84ab4/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum4 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum5
record = []
with open(os.getcwd() + '/2019-01-25T09-46-08-296Zdb4e3766c50ae5cf/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum5 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum6
record = []
with open(os.getcwd() + '/2019-01-25T09-48-17-311Z31caaaaa9c33ce70/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum6 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum7
record = []
with open(os.getcwd() + '/2019-01-25T09-51-02-833Zcc844e47f6fb70f5/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum7 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum8
record = []
with open(os.getcwd() + '/2019-01-25T09-53-13-820Z80b76f99a531cce7/Summary.OUT', 'r') as f:
    for row in f:
        record.append(row.strip())
        
summary = []
for i in range(4, len(record)):
    rec = record[i].split()
    summary.append(rec)

col = record[3].split()[1:]

summary = np.asarray(summary)
sum8 = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])

#sum9
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

"""
#190131 quantify the sensitivity of icrt against yield
"""

y_value = pd.concat([sum1["HWAH"], sum2["HWAH"], sum3["HWAH"], sum4["HWAH"], sum5["HWAH"], sum6["HWAH"], sum7["HWAH"], sum8["HWAH"], sum9["HWAH"]], axis=1).values.astype(np.int32)
y_df = pd.DataFrame(y_value, index=sum1.index, columns=["sum1", "sum2", "sum3", "sum4", "sum5", "sum6", "sum7", "sum8", "sum9"])

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

for i in range(3):
    ax.plot(np.arange(0, np.shape(y_df)[0], 1), y_df.iloc[:, i], color=cm.hsv(i/3))
    
sum_1, = plt.plot((1,1),(1,1), color=cm.hsv(0/3), linewidth=10)
sum_2, = plt.plot((1,1),(1,1), color=cm.hsv(1/3), linewidth=10)
sum_3, = plt.plot((1,1),(1,1), color=cm.hsv(2/3), linewidth=10)
#sum_4, = plt.plot((1,1),(1,1), color=cm.hsv(3/len(y_df.columns)), linewidth=10)
#sum_5, = plt.plot((1,1),(1,1), color=cm.hsv(4/len(y_df.columns)), linewidth=10)

plt.legend((sum_1, sum_2, sum_3),
           ("Previous root is 100kg/ha ("+repr(mean(y_df.iloc[:, 0]))+"kg/ha)", 
            "Previous root is 400kg/ha ("+repr(mean(y_df.iloc[:, 1]))+"kg/ha)",
            "Previous root is 700kg/ha ("+repr(mean(y_df.iloc[:, 2]))+"kg/ha)"), 
            fontsize=14, loc="best")

sum_1.set_visible(False)
sum_2.set_visible(False)
sum_3.set_visible(False)
#sum_4.set_visible(False)
#sum_5.set_visible(False)

plt.title("Sensitivity of Previous root weight", fontsize=17)
plt.xlabel("Sample ID", fontsize=15)
plt.ylabel("Final yield(kg/ha)", fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
ax.set_xlim(10, 40)
plt.savefig("190108_Reiton_RIX_png/190131_sensitvity_icrt.png", bbox_inches="tight")

plt.show()


"""
#190131 quantify the sensitivity of icres against yield
"""

y_value = pd.concat([sum1["HWAH"], sum2["HWAH"], sum3["HWAH"], sum4["HWAH"], sum5["HWAH"], sum6["HWAH"], sum7["HWAH"], sum8["HWAH"], sum9["HWAH"]], axis=1).values.astype(np.int32)
y_df = pd.DataFrame(y_value, index=sum1.index, columns=["sum1", "sum2", "sum3", "sum4", "sum5", "sum6", "sum7", "sum8", "sum9"])

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

for i in range(3,6):
    ax.plot(np.arange(0, np.shape(y_df)[0], 1), y_df.iloc[:, i], color=cm.hsv((i-3)/3))
    
sum_1, = plt.plot((1,1),(1,1), color=cm.hsv(0/3), linewidth=10)
sum_2, = plt.plot((1,1),(1,1), color=cm.hsv(1/3), linewidth=10)
sum_3, = plt.plot((1,1),(1,1), color=cm.hsv(2/3), linewidth=10)
#sum_4, = plt.plot((1,1),(1,1), color=cm.hsv(3/len(y_df.columns)), linewidth=10)
#sum_5, = plt.plot((1,1),(1,1), color=cm.hsv(4/len(y_df.columns)), linewidth=10)

plt.legend((sum_1, sum_2, sum_3),
           ("Previous residue is 100kg/ha ("+repr(mean(y_df.iloc[:, 3]))+"kg/ha)", 
            "Previous residue is 400kg/ha ("+repr(mean(y_df.iloc[:, 4]))+"kg/ha)",
            "Previous residue is 700kg/ha ("+repr(mean(y_df.iloc[:, 5]))+"kg/ha)"), 
            fontsize=14, loc="best")

sum_1.set_visible(False)
sum_2.set_visible(False)
sum_3.set_visible(False)
#sum_4.set_visible(False)
#sum_5.set_visible(False)

plt.title("Sensitivity of Previous residue weight", fontsize=17)
plt.xlabel("Sample ID", fontsize=15)
plt.ylabel("Final yield(kg/ha)", fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
ax.set_xlim(10, 40)
plt.savefig("190108_Reiton_RIX_png/190131_sensitvity_icres.png", bbox_inches="tight")

plt.show()


"""
#190131 quantify the sensitivity of icnd against yield
"""

y_value = pd.concat([sum1["HWAH"], sum2["HWAH"], sum3["HWAH"], sum4["HWAH"], sum5["HWAH"], sum6["HWAH"], sum7["HWAH"], sum8["HWAH"], sum9["HWAH"]], axis=1).values.astype(np.int32)
y_df = pd.DataFrame(y_value, index=sum1.index, columns=["sum1", "sum2", "sum3", "sum4", "sum5", "sum6", "sum7", "sum8", "sum9"])

fig = plt.figure(figsize=(12,6))
ax = fig.add_subplot(1,1,1)

for i in range(6,9):
    ax.plot(np.arange(0, np.shape(y_df)[0], 1), y_df.iloc[:, i], color=cm.hsv((i-6)/3))
    
sum_1, = plt.plot((1,1),(1,1), color=cm.hsv(0/3), linewidth=10)
sum_2, = plt.plot((1,1),(1,1), color=cm.hsv(1/3), linewidth=10)
sum_3, = plt.plot((1,1),(1,1), color=cm.hsv(2/3), linewidth=10)
#sum_4, = plt.plot((1,1),(1,1), color=cm.hsv(3/len(y_df.columns)), linewidth=10)
#sum_5, = plt.plot((1,1),(1,1), color=cm.hsv(4/len(y_df.columns)), linewidth=10)

plt.legend((sum_1, sum_2, sum_3),
           ("Previous nodule is 100kg/ha ("+repr(mean(y_df.iloc[:, 6]))+"kg/ha)", 
            "Previous nodule is 400kg/ha ("+repr(mean(y_df.iloc[:, 7]))+"kg/ha)",
            "Previous nodule is 700kg/ha ("+repr(mean(y_df.iloc[:, 8]))+"kg/ha)"), 
            fontsize=14, loc="best")

sum_1.set_visible(False)
sum_2.set_visible(False)
sum_3.set_visible(False)
#sum_4.set_visible(False)
#sum_5.set_visible(False)

plt.title("Sensitivity of Previous nodule weight", fontsize=17)
plt.xlabel("Sample ID", fontsize=15)
plt.ylabel("Final yield(kg/ha)", fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
ax.set_xlim(50, 100)
#plt.savefig("190108_Reiton_RIX_png/190131_sensitvity_icnd.png", bbox_inches="tight")

plt.show()


#generate histogram 
fig = plt.figure(figsize=(10,5))
ax = fig.add_subplot(1,1,1)

ax.hist(y_df.iloc[:,8].values, bins=50, cumulative=True, color='red', histtype="barstacked")

plt.title("Sensitivity of Previous nodule weight", fontsize=17)
plt.xlabel("Final yield(kg/ha)", fontsize=15)
plt.ylabel("Percentage(%)", fontsize=15)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
#ax.set_xlim(50, 100)
#plt.savefig("190108_Reiton_RIX_png/190131_sensitvity_icnd.png", bbox_inches="tight")

plt.show()









