#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 18 17:22:05 2018

@author: kameokashinichi
"""

"""
Function for generating weather scenario which reflects the seasonal forecast.
"""


import requests
import json
import pandas as pd
import os
import re
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
import math
from statistics import mean, stdev
from matplotlib.patches import Polygon
import matplotlib.cm as cm


forecast_dir = '/Users/kameokashinichi/Documents/postdoc/JMA_forecast_data/operational_3m/'
fdir = list(filter(lambda x: re.search('\d{8}$', x), os.listdir(forecast_dir)))
fdir.sort()

temptxt = '/Past_guid.txt'
raintxt = '/Prrr_guid.txt'
month = ['march', 'april', 'may', 'june', 'july', 'august', 'september']

def extractAnnualDirectory(year):
    """
    year: int (yyyy)
        the targeted year(2010-2018)
    """
    direc = list(filter(lambda x: re.search(repr(year)+'0[3-9]', x), fdir))
    return direc


def extract3monthBNNNAN(year):
    """
    from 2010 to 2018, we can apply this function.
    
    return dic : dict
        the dictionary which contains the ratio of BN:NN:AN
        .keys() -> ex. 'march_temperature'
        extract3monthBNNNAN(2010)['march_temperature'] is two demensional list of BN:NN:AN
        ex. "extract3monthBNNNAN(2010)['march_temperature'][0]" is the value of BN:NN:AN in april
    """
    
    print('generate forecast dictionary for {year}'.format(year=year))
    direc = extractAnnualDirectory(year)
    dic = dict()
    
    for i in range(len(direc)):        
        temp = []
        rain = []
        with open(forecast_dir+direc[i]+temptxt) as f:
            sp = f.read().split('\n')
            for l in range(len(sp)):
                a = sp[l].split(',')
                temp.append(a)
        
        tforecast = []
        for j in list([54, 88, 122]):
            t = temp[j][-6:-3]
            lis = [int(k) for k in t]
            tforecast.append(lis)
        
        dic.update({month[i]+"_temperature":tforecast})
        
        with open(forecast_dir+direc[i]+raintxt) as f:
            sp = f.read().split('\n')
            for l in range(len(sp)):
                a = sp[l].split(',')
                rain.append(a)
        
        rforecast = []
        for j in list([54, 88, 122]):
            r = rain[j][-6:-3]
            lis = [int(k) for k in r]
            rforecast.append(lis)
            
        dic.update({month[i]+"_precipitation":rforecast})
        
    return dic
         
def generateEdate(year, month):
    
    if month == 2:
        e_date = '{x}-{y:02}-28'.format(x=year, y=month)
    elif month == 4 or month == 6 or month == 9 or month == 11:
        e_date = '{x}-{y:02}-30'.format(x=year, y=month)
    else:
        e_date = '{x}-{y:02}-31'.format(x=year, y=month)
    
    return e_date


def generateKgenForecastScenario(scenario_num, year, month, ifid=False):
    """
    Kgen weather scenario for Agri Sasamoto applying seasonal forecast
    
    scenario_num : int
        number of the generated weather (for kgen, 500 is default)
    year : int
        the targeted year (from 2010 to 2018)
    month : int
        the targeted month (from 3 to 9)
    ifid : bool
        check if this function returns id or json result
    """
    
    url = "http://ec2-52-196-202-21.ap-northeast-1.compute.amazonaws.com/weather/generator/v1.1/scenarios"
    
    monthdic = {3: 'march',
                4: 'april',
                5: 'may',
                6: 'june',
                7: 'july',
                8: 'august',
                9: 'september'
                }
    
    fordict = extract3monthBNNNAN(year)
    
    forecast = {'monthly_forecasts': [{'b_date': '{x}-{y:02}-01'.format(x=year, y=month+1),
                            'e_date': generateEdate(year, month+1),
                            'type': 'average_air_temperature',
                            'probabilities': fordict[monthdic[month]+'_temperature'][0]},
                           {'b_date': '{x}-{y:02}-01'.format(x=year, y=month+1),
                            'e_date': generateEdate(year, month+1),
                            'type': 'precipitation',
                            'probabilities': fordict[monthdic[month]+'_precipitation'][0]},
                           {'b_date': '{x}-{y:02}-01'.format(x=year, y=month+2),
                            'e_date': generateEdate(year, month+2),
                            'type': 'average_air_temperature',
                            'probabilities': fordict[monthdic[month]+'_temperature'][1]},
                           {'b_date': '{x}-{y:02}-01'.format(x=year, y=month+2),
                            'e_date': generateEdate(year, month+2),
                            'type': 'precipitation',
                            'probabilities': fordict[monthdic[month]+'_precipitation'][1]},
                           {'b_date': '{x}-{y:02}-01'.format(x=year, y=month+3),
                            'e_date': generateEdate(year, month+3),
                            'type': 'average_air_temperature',
                            'probabilities': fordict[monthdic[month]+'_temperature'][2]},
                           {'b_date': '{x}-{y:02}-01'.format(x=year, y=month+3),
                            'e_date': generateEdate(year, month+3),
                            'type': 'precipitation',
                            'probabilities': fordict[monthdic[month]+'_precipitation'][2]}]
    }
    
    param = { 
      "wth_src" : "naro1km", 
      "wgen_model": "kgen",
      "scenario_num" : repr(scenario_num),
      "latitude" : "35.706179",
      "longitude" : "140.482362",
      "from_date" : "{x}-01-01".format(x=year),
      "to_date" : "{x}-12-31".format(x=year),
      "bn_nn_an" : "33:34:33",
      'jma_forecast_data': forecast,
      "monthly_adjust": True,
      "snow_adjust": False
      }
      
    headers = {
    'Content-Type': "application/json",
    'Cache-Control': "no-cache",
    'Postman-Token': "45ab4e0a-77e0-483d-9494-5f69124a3ba6"
    }
    
    payload = json.dumps(param)
    
    response = requests.request("POST", url, data=payload, headers=headers)
    rj = json.loads(response.text)
    print('The ID of the scenario for {x} in {y} is {z}'.format(x=monthdic[month], y=year, z=rj['ID']))
    
    if ifid == True:
        return rj['ID']
    else:
        return rj









