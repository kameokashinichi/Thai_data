#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 29 13:17:25 2018

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
from matplotlib.patches import Polygon
import matplotlib


"""
181229 generat calendar for Reitong farm
"""

month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug',
         'Sep', 'Oct', 'Nov', 'Dec', '']
variety = ['KDML105(transplant)','KDML105(sowing)','Red jasmine', 'Black rice']

fig = plt.figure(figsize=(10,3))
ax = fig.add_subplot(111)
plt.grid()
black = matplotlib.patches.Rectangle((140,60), 20, 20, color='red')
red = matplotlib.patches.Rectangle((165,30), 20, 20, color='red')
kdml = matplotlib.patches.Rectangle((200,0), 20, 20, color='red')
kt = matplotlib.patches.Rectangle((200,-30), 10, 20, color='red')
kt_1 = matplotlib.patches.Rectangle((210,-30), 10, 20, color='blue')
black2 = matplotlib.patches.Rectangle((160,60), 80, 20, color='green')
red2 = matplotlib.patches.Rectangle((185,30), 80, 20, color='green')
kdml2 = matplotlib.patches.Rectangle((220,0), 80, 20, color='green')
kt2 = matplotlib.patches.Rectangle((220,-30), 80, 20, color='green')
black3 = matplotlib.patches.Rectangle((240,60), 20, 20, color='orange')
red3 = matplotlib.patches.Rectangle((265,30), 20, 20, color='orange')
kdml3 = matplotlib.patches.Rectangle((300,0), 20, 20, color='orange')
kt3 = matplotlib.patches.Rectangle((300,-30), 20, 20, color='orange')

ax.add_patch(black)
ax.add_patch(red)
ax.add_patch(kdml)
ax.add_patch(kt)
ax.add_patch(kt_1)
ax.add_patch(black2)
ax.add_patch(red2)
ax.add_patch(kdml2)
ax.add_patch(kt2)
ax.add_patch(black3)
ax.add_patch(red3)
ax.add_patch(kdml3)
ax.add_patch(kt3)

seed,= ax.plot([1,1], color='red', linewidth=10)
grow,= ax.plot([1,1], color='green', linewidth=10)
harv,= ax.plot([1,1], color='orange', linewidth=10)
trans,= ax.plot([1,1], color='blue', linewidth=10)

plt.legend((seed, trans, grow, harv), ('sowing','transplanting','growing', 'harvest'), 
           fontsize=15,loc='best')

seed.set_visible(False)
grow.set_visible(False)
harv.set_visible(False)
trans.set_visible(False)

plt.title("The calendar of rice cultivation in Reitong farm", 
          fontsize=18)
plt.xticks(np.linspace(0, 365, 13), month)
plt.yticks(np.linspace(-20, 70, 4), variety)
plt.setp(ax.get_xticklabels(), fontsize=13, rotation=45, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=15, rotation=45, visible=True)
plt.xlim([0, 365])
plt.ylim([-30, 90])
plt.savefig("181224_Dssat_png/181229_calendar_of_rice_cultivation_in_Reitong_farm_trans", 
            bbox_inches="tight")
plt.show()




fig = plt.figure()
ax = fig.add_subplot(111)
rect1 = matplotlib.patches.Rectangle((-200,-100), 400, 200, color='yellow')
rect2 = matplotlib.patches.Rectangle((0,150), 300, 20, color='red')
rect3 = matplotlib.patches.Rectangle((-300,-50), 40, 200, color='#0099FF')
circle1 = matplotlib.patches.Circle((-200,-250), radius=90, color='#EB70AA')
ax.add_patch(rect1)
ax.add_patch(rect2)
ax.add_patch(rect3)
ax.add_patch(circle1)
plt.xlim([-400, 400])
plt.ylim([-400, 400])

plt.show()





















