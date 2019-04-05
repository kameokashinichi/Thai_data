#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 19 13:09:07 2019

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
import requests
import subprocess
import json


"""
190219 compare the result of wgen VS actual
"""

"""
190218 convert csv to payload

csv = pd.read_csv("190212_sumichem_with_weatherID.csv", header=0, index_col=0)

The columns of the csv is below

Index(['year', 'prefecture', 'field', 'latitude', 'longitude', 'variety',
       'sowing_date', 'transplanting_date', 'panicle_formation_date',
       'heading_date', 'proper_time_for_harvesting',
       'basal_nitrogen_kg_per_10a', 'WTH_ID', 'WTDE_ID'],
      dtype='object')

"""

def genTreatments(csv):
    """
    csv should be the dataset for single year.
    """
    treat = []
    for i in range(len(csv.index)):
        if csv.iloc[i, 11] == csv.iloc[i, 11]:
            trt = {
			"trt_num":repr(i+1),"rp":"0","sq":"0","op":"0","co":"0","r":"1","o":"0","c":"0","tname":"UNKNOWN","cu":"1","fl":repr(i+1),"sa":"0","ic":"0","mp":repr(i+1),"mi":"1","mf":repr(i+1),"mr":"0","mc":"0","mt":"0","me":"0","mh":"0","sm":"1"
            }
        else:
            trt = {
			"trt_num":repr(i+1),"rp":"0","sq":"0","op":"0","co":"0","r":"1","o":"0","c":"0","tname":"UNKNOWN","cu":"1","fl":repr(i+1),"sa":"0","ic":"0","mp":repr(i+1),"mi":"1","mf":"0","mr":"0","mc":"0","mt":"0","me":"0","mh":"0","sm":"1"
            }
            
        treat.append(trt)
        
    return treat

def genFields(csv):
    field = []
    for i in range(len(csv.index)):
        fl = {
        "l_num": repr(i+1),
        "id_field": "MOCK",
        "wsta": repr(i+1).zfill(4),
        "flsa": "-99",
        "flob": "0",
        "fldt": "DR000",
        "fldd": "0",
        "flds": "0",
        "flst": "00000",
        "sltx": "-99",
        "sldp": "100",
        "id_soil": "JP_NRPH10F",
        "flname": "-99",
        
        "xcrd": "0",
        "ycrd": "0",
        "elev": "0",
        "area": "0",
        "slen": "0",
        "flwr": "0",
        "slas": "0",
        "flhst": "-99",
        "fhdur": "-99"
        }
        field.append(fl)
        
    return field

def genPlantDetails(csv):
    Pdetail = []
    for i in range(len(csv.index)):
        pd = {
		"p_num":repr(i+1),
		"pdate":repr(csv.iloc[i, 7]),   
		"edate":"-99",
		"ppop":"70",
		"ppoe":"70",
		"plme":"T",   
		"plds":"R",
		"plrs":"80",
		"plrd":"0",
		"pldp":"5",
		"plwt":"-99",
		"page":"20",
		"penv":"25",
		"plph":"-99",
		"sprl":"0",
		"plname":"-99"
        }
        Pdetail.append(pd)
        
    return Pdetail

def genIrrigations(csv):
    irrig = []
    ir = {
            "ir_num": "1",
            "efir": "-99",
            "idep": "-99",
            "ithr": "-99",
            "iept": "-99",
            "ioff": "-99",
            "iame": "-99",
            "iamt": "1",
            "irname": "NONE",
            "operations": [
				{"idate":repr(min(csv.iloc[:,7])-3),"irop":"IR010","irval":"0"},
				{"idate":repr(min(csv.iloc[:,7])-3),"irop":"IR008","irval":"2"},
				{"idate":repr(min(csv.iloc[:,7])-3),"irop":"IR009","irval":"150"},
				{"idate":repr(min(csv.iloc[:,7])-3),"irop":"IR011","irval":"50"}
	    	]
		}
    irrig.append(ir)
    
    return irrig

def genFertilizers(csv):
    fert = []
    for i in range(len(csv.index)):
        if csv.iloc[i, 11] == csv.iloc[i, 11]:
            ft = {
           "f_num": repr(i+1),
           "fdate": repr(csv.iloc[i, 7]),
           "fmcd": "FE001",
           "facd": "AP001",
           "fdep": "5",
           "famn": repr(csv.iloc[i, 11]*10),
           "famp": "0",
           "famk": "0",
           "famc": "0",
           "famo": "0",
           "focd": "-99",
           "fername": "-99"
            }
            fert.append(ft)
            
        else:
            pass
        
    return fert

def genSimControls(csv):
    simcon = []
    sim = {
          "n_num": "1",
          "general": "GE",
          "nyers": "1",
          "nreps": "1",
          "start": "S",
          "sdate": repr(min(csv.iloc[:,7])-3),  
          "rseed": "2150",
          "sname": "UNKNOWN",
          "smodel": "",
          "options": "OP",
          "water": "Y",
          "nitro": "Y",
          "symbi": "N",
          "phosp": "N",
          "potas": "N",
          "dises": "N",
          "chem": "N",
          "till": "N",
          "co2": "M",
          "methods": "ME",
          "wther": "M",
          "incon": "M",
          "light": "E",
          "evapo": "R",
          "infil": "S",
          "photo": "C",
          "hydro": "R",
          "nswit": "1",
          "mesom": "P",
          "mesev": "S",
          "mesol": "2",
          "management": "MA",
          "plant": "R",
          "irrig": "R",
          "ferti": "R",
          "resid": "R",
          "harvs": "M",
          "outputs": "OU",
          "fname": "N",
          "ovvew": "Y",
          "sumry": "Y",
          "fropt": "1",
          "grout": "Y",
          "caout": "N",
          "waout": "Y",
          "niout": "Y",
          "miout": "N",
          "diout": "N",
          "vbose": "D",
          "chout": "N",
          "opout": "N",
          "planting": "PL",
          "pfrst": "85028",
          "plast": "85042",
          "ph2ol": "40",
          "ph2ou": "100",
          "ph2od": "30",
          "pstmx": "40",
          "pstmn": "10",
          "irrigation": "IR",
          "imdep": "30",
          "ithrl": "50",
          "ithru": "100",
          "iroff": "IB001",
          "imeth": "IB001",
          "iramt": "10",
          "ireff": "1",
          "nitrogen": "NI",
          "nmdep": "30",
          "nmthr": "50",
          "namnt": "25",
          "ncode": "IB001",
          "naoff": "IB001",
          "residues": "RE",
          "ripcn": "100",
          "rtime": "1",
          "ridep": "20",
          "harvest": "HA",
          "hfrst": "0",
          "hlast": "86035",
          "hpcnp": "100",
          "hpcnr": "0"	
		}
    
    simcon.append(sim)
    
    return simcon
            
            
                
def genPayloadFromCsv(csv, pdate, model="dssat", weather="http://dev.listenfield.com/cropsim/uploads/2019-02-13T02-13-10-403Z59d07631c33b41cd/weather_file2018.zip", file_name="190218_payload_test.json"):

    payload = {"planting_date": pdate,
      "crop_ident_ICASA": "RIC",
      "cultivar_name": "koshihikari",
      "model": model,
      "weather_file": weather,
      "wait": "true",
      "model_params":{
              "treatments":genTreatments(csv),
              "fields":genFields(csv),
              "planting_details":genPlantDetails(csv),
              "irrigations":genIrrigations(csv),
              "fertilizers":genFertilizers(csv),
              "simulation_controls":genSimControls(csv)}}
    
    
    with open(os.getcwd()+"/"+file_name, mode="w") as f:
        json.dump(payload, f, indent=4)

"""
sample code
genPayloadFromCsv(csv[csv["year"]==2018], pdate="2018-05-22", model="dssat", weather="http://dev.listenfield.com/cropsim/uploads/2019-02-13T02-13-10-403Z59d07631c33b41cd/weather_file2018.zip", file_name="190218_payload_test.json")

"""












