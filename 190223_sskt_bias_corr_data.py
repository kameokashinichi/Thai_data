#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Feb 23 10:59:57 2019

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
import json
import subprocess
from urllib import request
import zipfile

"""
190223 convert SRIS00xx.WTDE file into COMM00xx.WTDE and 00xx1801.WTH respectively

1. rename 100 "COMM00xx.WTDE file by using dataframe2wtd function
2. generate 100 "00xx1801.WTH" file by using "gencli.a" and "genWTH.a" via subprocess module
3. store these data into one directory
"""

#1. rename 100 "COMM00xx.WTDE file by using dataframe2wtd function

lis = list(filter(lambda x: re.search("COMM", x), os.listdir("./")))

os.chdir("Bias_corrected_WTDE")
for i in range(len(lis)):
    os.rename(lis[i], "COMM"+repr(i+1).zfill(4)+".WTDE")

#2. generate 100 "00xx1801.WTH" file by using "gencli.a" and "genWTH.a" via subprocess module
#3. store these data into one directory
for i in range(1, 101):
    #os.chdir("/Users/kameokashinichi/Documents/postdoc/crop_util")
    
    subprocess.call(["./genCLI.a", "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/COMM"+repr(i).zfill(4)+".WTDE",
                     repr(i).zfill(4), "15.000", "104.050", "4"])
    subprocess.call(["./genWTH.a", repr(i).zfill(4)+".CLI", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/COMM"+repr(i).zfill(4)+".WTDE"])
    subprocess.call(["mv", repr(i).zfill(4)+"1801.WTH", 
                     "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/Bias_corrected_WTDE/"])
    subprocess.call(["mv", repr(i).zfill(4)+".CLI", 
                     "./eunjin_cli/"])

    
"""
190223 simulate the date

weather_file -> "http://dev.listenfield.com:3232/cropsim/uploads/2019-02-23T03-03-44-228Zf03e556072c02591/Bias_corrected_WTDE.zip"
"""    
    
def generateDssatSSKT(pdate, w_file,  pmethod="S"):
    """
    pdate  : str (ex. 'yyyy-mm-dd')
        the transplanting date for simulation
    w_file : str
        the link of the weather scenario 
    pmethod: str
        "S"->Direct-sowing, "T"->Transplanting
        
    download result csv file
    """
    url = "http://dev.listenfield.com:3232/cropsim/v1.1/simulations"
    
    payload = {
  "planting_date": pdate,
  "crop_ident_ICASA": "RIC",
  "cultivar_name": "KDML105",
  "model": "dssat",
  "weather_file": w_file,
  "wait": "true",
  "model_params": 
  {
    "id_soil": "JP_NRPH10F",
    "initial_conditions":[
      {
        "ic_num": "1",
        "pcr": "SB",
        "icdat": repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),   
        "icrt": "100",
        "icnd": "100",
        "icrn": "1",
        "icre": "1",
        "icwd": "-99",
        "icres": "100",   
        "icren": "0.8",
        "icrep": "0",
        "icrip": "100",
        "icrid": "15",
        "icname": "-99",
        "base_layers": [
          { "icbl": "5", "sh2o": "0.05", "snh4": "2.50", "sno3": "7.14" },
          { "icbl": "15", "sh2o": "0.07", "snh4": "2.57", "sno3": "4.66" },
          { "icbl": "30", "sh2o": "0.05", "snh4": "0.04", "sno3": "3.88" },
          { "icbl": "42", "sh2o": "0.04", "snh4": "0.07", "sno3": "3.71" },
          { "icbl": "55", "sh2o": "0.04", "snh4": "0.03", "sno3": "1.37" },
          { "icbl": "67", "sh2o": "0.05", "snh4": "0.01", "sno3": "0.98" },
          { "icbl": "80", "sh2o": "0.07", "snh4": "0.01", "sno3": "1.06" },
          { "icbl": "100", "sh2o": "0.05", "snh4": "0.01", "sno3": "1.23" }
        ]
      }
    ],
        "planting_details":[
    	{
		"p_num":"1",
		"pdate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])),   
		"edate":"-99",
		"ppop":"6.2",
		"ppoe":"6.2",
		"plme":pmethod,   
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
	],
    "irrigations":[
    {
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
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR010","irval":"0"},
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR008","irval":"2"},
				{"idate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),"irop":"IR009","irval":"150"}
	    	]
		}
	],
    "residues":[
		{
		"r_num":"1",
		"rdate":repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),
		"rcod":"RE999",
        "ramt": "600",
        "resn": "3.5",
        "resp": "0.5",
        "resk": "-99",
        "rinp": "-99",
        "rdep": "15",
        "rmet": "-99",
        "rename": "-99"
		}
      ],
    "simulation_controls":[
		{
          "n_num": "1",
          "general": "GE",
          "nyers": "1",
          "nreps": "1",
          "start": "S",
          "sdate": repr(DATE2DOY(pdate)+1000*int(pdate[2:4])-7),  
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
    ]      
  }
}   
        
    headers = {
        'Content-Type': "application/json",
        'Cache-Control': "no-cache",
        'Postman-Token': "a65dd381-a65c-43d7-80f9-a183d50bd3f4"
        }
    
    payload = json.dumps(payload)
    
    response = requests.request("POST", url, data=payload, headers=headers)

    jinfo = json.loads(response.text)
    #csvlink = jinfo['csv_output']
    
    #print(type(csvlink))
    #request.urlretrieve(csvlink, folder + jinfo["id"] + '.csv')
    return jinfo


def getDssatData(jinfo, folder):
    """
    jinfo : dict
        the json file from Dssat API
    folder: str
        the name of the folder which stores data of the result
    """
    path = "/Users/kameokashinichi/Documents/postdoc/listenfield/Thai data/"
    
    os.mkdir(path+folder+"/"+jinfo["id"])
    print(jinfo["id"])
    
    outputs = re.sub(":3232", "", jinfo['output_directory'])
    
    request.urlretrieve(outputs+"/Summary.OUT", path+folder+"/"+jinfo["id"]+"/"+"/Summary.OUT")
    request.urlretrieve(outputs+"/JPRI0001.RIX", path+folder+"/"+jinfo["id"]+"/"+"/JPRI0001.RIX")    
    request.urlretrieve(outputs+"/PlantGro.OUT", path+folder+"/"+jinfo["id"]+"/"+"/PlantGro.OUT")    
    request.urlretrieve(outputs+"/PlantN.OUT", path+folder+"/"+jinfo["id"]+"/"+"/PlantN.OUT")    
    request.urlretrieve(outputs+"/SoilNi.OUT", path+folder+"/"+jinfo["id"]+"/"+"/SoilNi.OUT")
    request.urlretrieve(outputs+"/SoilWat.OUT", path+folder+"/"+jinfo["id"]+"/"+"/SoilWat.OUT")



#run dssat API
os.mkdir("190223_sskt_cumudata_bias_corr_wgen")

ds_date = ["2015-05-03", "2015-05-13", "2015-05-23", "2015-06-02", "2015-06-12", 
           "2015-06-22", "2015-07-02", "2015-07-12"]
tp_date = ["2015-05-23", "2015-06-02", "2015-06-12", 
           "2015-06-22", "2015-07-02", "2015-07-12", "2015-07-22", "2015-08-01"]


for i in range(0, 2):
    if i == 0:
        for j in range(1, len(ds_date)):
            jinfo = generateDssatSSKT(ds_date[j], "http://dev.listenfield.com/cropsim/uploads/2019-02-23T03-03-44-228Zf03e556072c02591/Bias_corrected_WTDE.zip",  pmethod="S")
            getDssatData(jinfo, "190223_sskt_cumudata_bias_corr_wgen")
    else:
        for j in range(len(tp_date)):
            jinfo = generateDssatSSKT(tp_date[j], "http://dev.listenfield.com/cropsim/uploads/2019-02-23T03-03-44-228Zf03e556072c02591/Bias_corrected_WTDE.zip",  pmethod="T")
            getDssatData(jinfo, "190223_sskt_cumudata_bias_corr_wgen")        


    
"""
Direct-sowing in 18123 -> "2019-02-23T04-46-58-933Z2ceabf44db5dcf78"
Direct-sowing in 18133 -> "2019-02-23T05-24-31-852Zb88764acb3667f91"
Direct-sowing in 18143 -> "2019-02-23T05-24-45-686Z8543f7b824ceba97"
Direct-sowing in 18153 -> "2019-02-23T05-25-07-267Z2d176d027474a535"
Direct-sowing in 18163 -> "2019-02-23T05-25-19-155Zf8045283dc860161"
Direct-sowing in 18173 -> "2019-02-23T05-25-31-011Zaad911c3fb980f06"
Direct-sowing in 18183 -> "2019-02-23T05-25-42-479Z8794f3edc3de886f"
Direct-sowing in 18193 -> "2019-02-23T05-25-53-301Z6c3bdde7c3608348"
Transplanting in 18143 -> "2019-02-23T05-26-03-993Zf834b4268740f7dc"
Transplanting in 18153 -> "2019-02-23T05-26-15-859Z82511d2847cf9854"
Transplanting in 18163 -> "2019-02-23T05-26-26-977Z68682812829185b1"
Transplanting in 18173 -> "2019-02-23T05-26-38-286Z6f85a68c760df954"
Transplanting in 18183 -> "2019-02-23T05-26-50-097Z127a47a1f383e8d5"
Transplanting in 18193 -> "2019-02-23T05-27-00-944Z8d93edca97e5a640"
Transplanting in 18203 -> "2019-02-23T05-27-11-116Z9a9fd16aea7b4eaa"
Transplanting in 18213 -> "2019-02-23T05-27-21-262Zbe3739b479f842bb"
"""

ds_id = ["2019-02-23T04-46-58-933Z2ceabf44db5dcf78","2019-02-23T05-24-31-852Zb88764acb3667f91",
         "2019-02-23T05-24-45-686Z8543f7b824ceba97","2019-02-23T05-25-07-267Z2d176d027474a535",
         "2019-02-23T05-25-19-155Zf8045283dc860161","2019-02-23T05-25-31-011Zaad911c3fb980f06",
         "2019-02-23T05-25-42-479Z8794f3edc3de886f","2019-02-23T05-25-53-301Z6c3bdde7c3608348"]

tp_id = ["2019-02-23T05-26-03-993Zf834b4268740f7dc","2019-02-23T05-26-15-859Z82511d2847cf9854",
         "2019-02-23T05-26-26-977Z68682812829185b1","2019-02-23T05-26-38-286Z6f85a68c760df954",
         "2019-02-23T05-26-50-097Z127a47a1f383e8d5","2019-02-23T05-27-00-944Z8d93edca97e5a640",
         "2019-02-23T05-27-11-116Z9a9fd16aea7b4eaa","2019-02-23T05-27-21-262Zbe3739b479f842bb"]

#generate list which consists of the dataframe of Direct-sowing result
dslist = []
dserr = []
for i in range(len(ds_id)):
    record = []
    with open(os.getcwd() + '/190223_sskt_cumudata_bias_corr_wgen/'+ds_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
    
    summary = []
    err = []    
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
        else:
            err.append(i-3)
            
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    dslist.append(df)
    dserr.append(err)


#generate list which consists of the dataframe of Transplanting result
tplist = []
tperr = []
for i in range(len(tp_id)):
    record = []
    with open(os.getcwd() + '/190223_sskt_cumudata_bias_corr_wgen/'+tp_id[i]+'/Summary.OUT', 'r') as f:
        for row in f:
            record.append(row.strip())
    
    summary = []
    err = []
    for i in range(4, len(record)):
        rec = record[i].split()
        if len(rec) == 82:
            summary.append(rec)
        else:
            err.append(i-3)
            
    col = record[3].split()[1:]
    
    summary = np.asarray(summary)
    sum_df5T = pd.DataFrame(summary[:, 1:], index=summary[:, 0], columns=col[1:])
    
    val = sum_df5T[["PDAT", "HWAH", "ADAT", "MDAT"]].values.astype(np.int32)
    df = pd.DataFrame(val, index=np.arange(1, len(sum_df5T.index)+1), columns=["PDAT", "HWAH", "ADAT", "MDAT"])
    tplist.append(df)
    tperr.append(err)



os.mkdir("190223_sskt_bcorrwgen_yield_png")

#compare these two ~tpdate == 18123~
order0 = dslist[0].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[0], ord_df0], axis=1, sort=True)
order1 = tplist[0].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[0], ord_df1], axis=1, sort=True)

val0 = dslist[0]['HWAH'].values.astype(np.float32)
val1 = tplist[0]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

#yy1_0 = float(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)]),'HWAH'])*0.7
yy2_0 = float(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[0].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[0].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[0].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[0].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[0].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[0].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[0].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[0].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
ax.set_xlim(2500, 6000)
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index)+5)
#ax2.set_ylim(0, len(sum_ds1.index)+5)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18123_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~tpdate == 18133~
order0 = dslist[1].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[1], ord_df0], axis=1, sort=True)
order1 = tplist[1].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[1], ord_df1], axis=1, sort=True)

val0 = dslist[1]['HWAH'].values.astype(np.float32)
val1 = tplist[1]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[1].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[1].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[1].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[1].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[1].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[1].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[1].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[1].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 6000)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18133_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the late May~
order0 = dslist[2].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[2], ord_df0], axis=1, sort=True)
order1 = tplist[2].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[2], ord_df1], axis=1, sort=True)

val0 = dslist[2]['HWAH'].values.astype(np.float32)
val1 = tplist[2]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3500

yy1_0 = float(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[2].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[2].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[2].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[2].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[2].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[2].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[2].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[2].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late May", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram(transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2500, 6000)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18143_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the early June~
order0 = dslist[3].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[3], ord_df0], axis=1, sort=True)
order1 = tplist[3].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[3], ord_df1], axis=1, sort=True)

val0 = dslist[3]['HWAH'].values.astype(np.float32)
val1 = tplist[3]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[3].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[3].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[3].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[3].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[3].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[3].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[3].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[3].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, round(10000/len(sum_ds0.index)), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/len(sum_ds1.index)), 6).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#ax.set_ylim(0, len(sum_ds0.index))
#ax2.set_ylim(0, len(sum_ds1.index))
ax.set_xlim(2000, 5500)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18153_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle June~
order0 = dslist[4].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[4], ord_df0], axis=1, sort=True)
order1 = tplist[4].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[4], ord_df1], axis=1, sort=True)

val0 = dslist[4]['HWAH'].values.astype(np.float32)
val1 = tplist[4]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3200

yy1_0 = float(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[4].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[4].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[4].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[4].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[4].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[4].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[4].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[4].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 82, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 5500)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18163_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the late June~
order0 = dslist[5].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[5], ord_df0], axis=1, sort=True)
order1 = tplist[5].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[5], ord_df1], axis=1, sort=True)

val0 = dslist[5]['HWAH'].values.astype(np.float32)
val1 = tplist[5]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[5].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[5].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[5].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[5].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[5].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[5].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[5].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[5].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in late June", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 82, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(2000, 5000)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18173_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the early July~
order0 = dslist[6].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[6], ord_df0], axis=1, sort=True)
order1 = tplist[6].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[6], ord_df1], axis=1, sort=True)

val0 = dslist[6]['HWAH'].values.astype(np.float32)
val1 = tplist[6]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 3000

yy1_0 = float(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[6].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[6].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[6].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[6].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[6].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[6].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[6].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[6].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in early July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 83, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 84, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4500)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18183_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


#compare these two ~the middle July~
order0 = dslist[7].sort_values("HWAH").index
ord_df0 = pd.DataFrame(np.arange(1,len(order0)+1), index=order0, columns=['ORDER'])
sum_ds0 = pd.concat([dslist[7], ord_df0], axis=1, sort=True)
order1 = tplist[7].sort_values("HWAH").index
ord_df1 = pd.DataFrame(np.arange(1,len(order1)+1), index=order1, columns=['ORDER'])
sum_ds1 = pd.concat([tplist[7], ord_df1], axis=1, sort=True)

val0 = dslist[7]['HWAH'].values.astype(np.float32)
val1 = tplist[7]['HWAH'].values.astype(np.float32)

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

thres = 2500

yy1_0 = float(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_0 = float(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind0 = np.abs(val0 - yy1_0).argmin()+1
Ind0 = np.abs(val0 - thres).argmin()+1 
yy1_1 = float(tplist[7].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.7
yy2_1 = float(tplist[7].loc[order1[round(50*len(sum_ds0.index)/100)],'HWAH'])*0.2
#Ind1 = np.abs(val1 - yy1_1).argmin()+1
Ind1 = np.abs(val1 - thres).argmin()+1 

ax.hist(val0, bins=50, cumulative=True, color='red', histtype="barstacked")

ax.plot([min(val0), max(val1)],[round(20*len(sum_ds0.index)/100), round(20*len(sum_ds0.index)/100)], color="black", label="20 percentile Yield="+repr(dslist[7].loc[order0[round(20*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(50*len(sum_ds0.index)/100), round(50*len(sum_ds0.index)/100)], color="blue", label="50 percentile Yield="+repr(dslist[7].loc[order0[round(50*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([min(val0), max(val1)],[round(80*len(sum_ds0.index)/100), round(80*len(sum_ds0.index)/100)], color="orange", label="80 percentile Yield="+repr(dslist[7].loc[order0[round(80*len(sum_ds0.index)/100)],'HWAH'])+"kg/ha")
ax.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds0.loc[Ind0,"ORDER"]/len(sum_ds0.index)*100))+"%")
ax.legend(loc="best", fontsize=14)

ax2.hist(val1, bins=50, cumulative=True, color='red', histtype="barstacked")

ax2.plot([min(val0), max(val1)],[round(20*len(sum_ds1.index)/100), round(20*len(sum_ds1.index)/100)], color="black", label="20 percentile Yield="+repr(tplist[7].loc[order1[round(20*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(50*len(sum_ds1.index)/100), round(50*len(sum_ds1.index)/100)], color="blue", label="50 percentile Yield="+repr(tplist[7].loc[order1[round(50*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([min(val0), max(val1)],[round(80*len(sum_ds1.index)/100), round(80*len(sum_ds1.index)/100)], color="orange", label="80 percentile Yield="+repr(tplist[7].loc[order1[round(80*len(sum_ds1.index)/100)],'HWAH'])+"kg/ha")
ax2.plot([thres, thres],[0,100], color="green", label="The Risk of Lower than " +repr(thres)+ "(kg/ha) = "+repr(round(sum_ds1.loc[Ind1,"ORDER"]/len(sum_ds1.index)*100))+"%")
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Yield(Direct-sowing) in middle July", fontsize=18)
#ax.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_title("The Cumulative Histogram (transplanting) -WGEN_BCORR-", fontsize=18)
ax2.set_xlabel("The yield of the simulation result(kg/ha)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
plt.setp(ax.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
ax.set_ylim(0, len(sum_ds0.index)+5)
ax2.set_ylim(0, len(sum_ds1.index)+5)
ax.set_xlim(1500, 4500)
#plt.savefig("190223_sskt_bcorrwgen_yield_png/190223_CDF_Reiton_Yield_TP_VS_DS_18193_WGEN_BCORR.png", bbox_inches='tight')

plt.show()


"""
#MATURITY DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190223_sskt_bcorrwgen_mdat_png")

order0=dslist[0].sort_values("MDAT").index
order1=tplist[0].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[0].index)+1):
    if dslist[0]['MDAT'][i] < 2016000:
        val = dslist[0]['MDAT'][i] - 2015000
    else:
        val = dslist[0]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[0].index)+1):
    if tplist[0]['MDAT'][i] < 2016000:
        val = tplist[0]['MDAT'][i] - 2015000
    else:
        val = tplist[0]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[0].index)*0.2
val50_0 = len(dslist[0].index)*0.5
val80_0 = len(dslist[0].index)*0.8
val20_1 = len(tplist[0].index)*0.2
val50_1 = len(tplist[0].index)*0.5
val80_1 = len(tplist[0].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(20*len(dslist[0].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(50*len(dslist[0].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[0].loc[order0[round(80*len(dslist[0].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(20*len(tplist[0].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(50*len(tplist[0].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[0].loc[order1[round(80*len(tplist[0].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(280, 340, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(280, 340, 10)))
ax.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax.set_xlim(280, 330)
ax2.set_xlim(280, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate123.png", bbox_inches='tight')
plt.show()


#Maturity date in 18133
order0=dslist[1].sort_values("MDAT").index
order1=tplist[1].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[1].index)+1):
    if dslist[1]['MDAT'][i] < 2016000:
        val = dslist[1]['MDAT'][i] - 2015000
    else:
        val = dslist[1]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[1].index)+1):
    if tplist[1]['MDAT'][i] < 2016000:
        val = tplist[1]['MDAT'][i] - 2015000
    else:
        val = tplist[1]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[1].index)*0.2
val50_0 = len(dslist[1].index)*0.5
val80_0 = len(dslist[1].index)*0.8
val20_1 = len(tplist[1].index)*0.2
val50_1 = len(tplist[1].index)*0.5
val80_1 = len(tplist[1].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(20*len(dslist[1].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(50*len(dslist[1].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[1].loc[order0[round(80*len(dslist[1].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(20*len(tplist[1].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(50*len(tplist[1].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[1].loc[order1[round(80*len(tplist[1].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(290, 350, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(290, 350, 5)))
ax.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax.set_xlim(290, 335)
ax2.set_xlim(290, 335)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate133.png", bbox_inches='tight')
plt.show()


#Maturity date in 18143
order0=dslist[2].sort_values("MDAT").index
order1=tplist[2].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[2].index)+1):
    if dslist[2]['MDAT'][i] < 2016000:
        val = dslist[2]['MDAT'][i] - 2015000
    else:
        val = dslist[2]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[2].index)+1):
    if tplist[2]['MDAT'][i] < 2016000:
        val = tplist[2]['MDAT'][i] - 2015000
    else:
        val = tplist[2]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[2].index)*0.2
val50_0 = len(dslist[2].index)*0.5
val80_0 = len(dslist[2].index)*0.8
val20_1 = len(tplist[2].index)*0.2
val50_1 = len(tplist[2].index)*0.5
val80_1 = len(tplist[2].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(20*len(dslist[2].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(50*len(dslist[2].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[2].loc[order0[round(80*len(dslist[2].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(20*len(tplist[2].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(50*len(tplist[2].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[2].loc[order1[round(80*len(tplist[2].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(290, 350, 10)))
ax.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, round(10000/100), 6).astype(np.int32))
ax.set_xlim(290, 340)
ax2.set_xlim(290, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate143.png", bbox_inches='tight')
plt.show()


#Maturity date in 18153
order0=dslist[3].sort_values("MDAT").index
order1=tplist[3].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[3].index)+1):
    if dslist[3]['MDAT'][i] < 2016000:
        val = dslist[3]['MDAT'][i] - 2015000
    else:
        val = dslist[3]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[3].index)+1):
    if tplist[3]['MDAT'][i] < 2016000:
        val = tplist[3]['MDAT'][i] - 2015000
    else:
        val = tplist[3]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[3].index)*0.2
val50_0 = len(dslist[3].index)*0.5
val80_0 = len(dslist[3].index)*0.8
val20_1 = len(tplist[3].index)*0.2
val50_1 = len(tplist[3].index)*0.5
val80_1 = len(tplist[3].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(20*len(dslist[3].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(50*len(dslist[3].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[3].loc[order0[round(80*len(dslist[3].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(20*len(tplist[3].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(50*len(tplist[3].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[3].loc[order1[round(80*len(tplist[3].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(300, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(300, 345, 5)))
ax.set_yticklabels(np.linspace(0, 100, 6).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax.set_xlim(300, 340)
ax2.set_xlim(300, 340)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate153.png", bbox_inches='tight')
plt.show()


#Maturity date in 18163
order0=dslist[4].sort_values("MDAT").index
order1=tplist[4].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[4].index)+1):
    if dslist[4]['MDAT'][i] < 2016000:
        val = dslist[4]['MDAT'][i] - 2015000
    else:
        val = dslist[4]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[4].index)+1):
    if tplist[4]['MDAT'][i] < 2016000:
        val = tplist[4]['MDAT'][i] - 2015000
    else:
        val = tplist[4]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[4].index)*0.2
val50_0 = len(dslist[4].index)*0.5
val80_0 = len(dslist[4].index)*0.8
val20_1 = len(tplist[4].index)*0.2
val50_1 = len(tplist[4].index)*0.5
val80_1 = len(tplist[4].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(20*len(dslist[4].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(50*len(dslist[4].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[4].loc[order0[round(80*len(dslist[4].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(20*len(tplist[4].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(50*len(tplist[4].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[4].loc[order1[round(80*len(tplist[4].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(305, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(305, 345, 5)))
ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax.set_xlim(305, 340)
ax2.set_xlim(305, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate163.png", bbox_inches='tight')
plt.show()


#Maturity date in 18173
order0=dslist[5].sort_values("MDAT").index
order1=tplist[5].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[5].index)+1):
    if dslist[5]['MDAT'][i] < 2016000:
        val = dslist[5]['MDAT'][i] - 2015000
    else:
        val = dslist[5]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[5].index)+1):
    if tplist[5]['MDAT'][i] < 2016000:
        val = tplist[5]['MDAT'][i] - 2015000
    else:
        val = tplist[5]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[5].index)*0.2
val50_0 = len(dslist[5].index)*0.5
val80_0 = len(dslist[5].index)*0.8
val20_1 = len(tplist[5].index)*0.2
val50_1 = len(tplist[5].index)*0.5
val80_1 = len(tplist[5].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(20*len(dslist[5].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(50*len(dslist[5].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[5].loc[order0[round(80*len(dslist[5].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(20*len(tplist[5].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(50*len(tplist[5].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[5].loc[order1[round(80*len(tplist[5].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(310, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(310, 345, 5)))
ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 82, 5).astype(np.int32))
ax.set_xlim(310, 340)
ax2.set_xlim(310, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate173.png", bbox_inches='tight')
plt.show()


#Maturity date in 18183
order0=dslist[6].sort_values("MDAT").index
order1=tplist[6].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[6].index)+1):
    if dslist[6]['MDAT'][i] < 2016000:
        val = dslist[6]['MDAT'][i] - 2015000
    else:
        val = dslist[6]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[6].index)+1):
    if tplist[6]['MDAT'][i] < 2016000:
        val = tplist[6]['MDAT'][i] - 2015000
    else:
        val = tplist[6]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[6].index)*0.2
val50_0 = len(dslist[6].index)*0.5
val80_0 = len(dslist[6].index)*0.8
val20_1 = len(tplist[6].index)*0.2
val50_1 = len(tplist[6].index)*0.5
val80_1 = len(tplist[6].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(20*len(dslist[6].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(50*len(dslist[6].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[6].loc[order0[round(80*len(dslist[6].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(20*len(tplist[6].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(50*len(tplist[6].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[6].loc[order1[round(80*len(tplist[6].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax.set_yticklabels(np.linspace(0, 83, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 85, 5).astype(np.int32))
ax.set_xlim(315, 340)
ax2.set_xlim(315, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate183.png", bbox_inches='tight')
plt.show()


#Maturity date in 18193
order0=dslist[7].sort_values("MDAT").index
order1=tplist[7].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

mdat0 = []
for i in range(1, len(dslist[7].index)+1):
    if dslist[7]['MDAT'][i] < 2016000:
        val = dslist[7]['MDAT'][i] - 2015000
    else:
        val = dslist[7]['MDAT'][i] - 2016000+365
    mdat0.append(val)

mdat1 = []
for i in range(1, len(tplist[7].index)+1):
    if tplist[7]['MDAT'][i] < 2016000:
        val = tplist[7]['MDAT'][i] - 2015000
    else:
        val = tplist[7]['MDAT'][i] - 2016000+365
    mdat1.append(val)

val20_0 = len(dslist[7].index)*0.2
val50_0 = len(dslist[7].index)*0.5
val80_0 = len(dslist[7].index)*0.8
val20_1 = len(tplist[7].index)*0.2
val50_1 = len(tplist[7].index)*0.5
val80_1 = len(tplist[7].index)*0.8

ax.hist(np.asarray(mdat0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(mdat0)-10, max(mdat0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(20*len(dslist[7].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(50*len(dslist[7].index)/100)],'MDAT']-2015000))
ax.plot([min(mdat0)-10, max(mdat0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(dslist[7].loc[order0[round(80*len(dslist[7].index)/100)],'MDAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(mdat1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(20*len(tplist[7].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(50*len(tplist[7].index)/100)],'MDAT']-2015000))
ax2.plot([min(mdat0)-10, max(mdat0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile MDAT="+DOY2DATE(tplist[7].loc[order1[round(80*len(tplist[7].index)/100)],'MDAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Maturity date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Wgen-", fontsize=18)
ax2.set_xlabel("The maturity date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(315, 345, 5)))
ax.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
ax.set_xlim(315, 340)
ax2.set_xlim(315, 340)
ax.set_ylim(0, len(mdat0)+5)
ax2.set_ylim(0, len(mdat1)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_mdat_png/190223_CDF_SSKT_WgenBcorr_Maturity_pdate193.png", bbox_inches='tight')
plt.show()


"""
#ANTHESIS DATE, direct-sowing pattern -Wgen-
"""
os.mkdir("190223_sskt_bcorrwgen_adat_png")

order0=dslist[0].sort_values("ADAT").index
order1=tplist[0].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[0].index)+1):
    if dslist[0]['ADAT'][i] < 2016000:
        val = dslist[0]['ADAT'][i] - 2015000
    else:
        val = dslist[0]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[0].index)+1):
    if tplist[0]['ADAT'][i] < 2016000:
        val = tplist[0]['ADAT'][i] - 2015000
    else:
        val = tplist[0]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[0].index)*0.2
val50_0 = len(dslist[0].index)*0.5
val80_0 = len(dslist[0].index)*0.8
val20_1 = len(tplist[0].index)*0.2
val50_1 = len(tplist[0].index)*0.5
val80_1 = len(tplist[0].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(20*len(dslist[0].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(50*len(dslist[0].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[0].loc[order0[round(80*len(dslist[0].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(20*len(tplist[0].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(50*len(tplist[0].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[0].loc[order1[round(80*len(tplist[0].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early May -Wgen-", fontsize=18)
ax2.set_xlabel("The anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-6, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+5)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate123.png", bbox_inches='tight')
plt.show()


#Maturity date in 18133
order0=dslist[1].sort_values("ADAT").index
order1=tplist[1].sort_values("MDAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[1].index)+1):
    if dslist[1]['ADAT'][i] < 2016000:
        val = dslist[1]['ADAT'][i] - 2015000
    else:
        val = dslist[1]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[1].index)+1):
    if tplist[1]['ADAT'][i] < 2016000:
        val = tplist[1]['ADAT'][i] - 2015000
    else:
        val = tplist[1]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[1].index)*0.2
val50_0 = len(dslist[1].index)*0.5
val80_0 = len(dslist[1].index)*0.8
val20_1 = len(tplist[1].index)*0.2
val50_1 = len(tplist[1].index)*0.5
val80_1 = len(tplist[1].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(20*len(dslist[1].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(50*len(dslist[1].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[1].loc[order0[round(80*len(dslist[1].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(20*len(tplist[1].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(50*len(tplist[1].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[1].loc[order1[round(80*len(tplist[1].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)


ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-12, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
ax2.set_xlim(min(ADAT0)-5, max(ADAT0)+2)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate133.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18143
order0=dslist[2].sort_values("ADAT").index
order1=tplist[2].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[2].index)+1):
    if dslist[2]['ADAT'][i] < 2016000:
        val = dslist[2]['ADAT'][i] - 2015000
    else:
        val = dslist[2]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[2].index)+1):
    if tplist[2]['ADAT'][i] < 2016000:
        val = tplist[2]['ADAT'][i] - 2015000
    else:
        val = tplist[2]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[2].index)*0.2
val50_0 = len(dslist[2].index)*0.5
val80_0 = len(dslist[2].index)*0.8
val20_1 = len(tplist[2].index)*0.2
val50_1 = len(tplist[2].index)*0.5
val80_1 = len(tplist[2].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(20*len(dslist[2].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(50*len(dslist[2].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[2].loc[order0[round(80*len(dslist[2].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(20*len(tplist[2].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(50*len(tplist[2].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[2].loc[order1[round(80*len(tplist[2].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 323)
ax2.set_xlim(min(ADAT0)-5, 323)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate143.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18153
order0=dslist[3].sort_values("ADAT").index
order1=tplist[3].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[3].index)+1):
    if dslist[3]['ADAT'][i] < 2016000:
        val = dslist[3]['ADAT'][i] - 2015000
    else:
        val = dslist[3]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[3].index)+1):
    if tplist[3]['ADAT'][i] < 2016000:
        val = tplist[3]['ADAT'][i] - 2015000
    else:
        val = tplist[3]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[3].index)*0.2
val50_0 = len(dslist[3].index)*0.5
val80_0 = len(dslist[3].index)*0.8
val20_1 = len(tplist[3].index)*0.2
val50_1 = len(tplist[3].index)*0.5
val80_1 = len(tplist[3].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(20*len(dslist[3].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(50*len(dslist[3].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[3].loc[order0[round(80*len(dslist[3].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(20*len(tplist[3].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(50*len(tplist[3].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[3].loc[order1[round(80*len(tplist[3].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early June -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-14, max(ADAT0)+20, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-14, max(ADAT0)+20, 10)))
ax.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate153.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18163
order0=dslist[4].sort_values("ADAT").index
order1=tplist[4].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[4].index)+1):
    if dslist[4]['ADAT'][i] < 2016000:
        val = dslist[4]['ADAT'][i] - 2015000
    else:
        val = dslist[4]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[4].index)+1):
    if tplist[4]['ADAT'][i] < 2016000:
        val = tplist[4]['ADAT'][i] - 2015000
    else:
        val = tplist[4]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[4].index)*0.2
val50_0 = len(dslist[4].index)*0.5
val80_0 = len(dslist[4].index)*0.8
val20_1 = len(tplist[4].index)*0.2
val50_1 = len(tplist[4].index)*0.5
val80_1 = len(tplist[4].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(20*len(dslist[4].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(50*len(dslist[4].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[4].loc[order0[round(80*len(dslist[4].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(20*len(tplist[4].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(50*len(tplist[4].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[4].loc[order1[round(80*len(tplist[4].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle June -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 10)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-9, max(ADAT0)+10, 10)))
ax.set_yticklabels(np.linspace(0, 80, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 330)
ax2.set_xlim(min(ADAT0)-5, 330)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate163.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18173
order0=dslist[5].sort_values("ADAT").index
order1=tplist[5].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[5].index)+1):
    if dslist[5]['ADAT'][i] < 2016000:
        val = dslist[5]['ADAT'][i] - 2015000
    else:
        val = dslist[5]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[5].index)+1):
    if tplist[5]['ADAT'][i] < 2016000:
        val = tplist[5]['ADAT'][i] - 2015000
    else:
        val = tplist[5]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[5].index)*0.2
val50_0 = len(dslist[5].index)*0.5
val80_0 = len(dslist[5].index)*0.8
val20_1 = len(tplist[5].index)*0.2
val50_1 = len(tplist[5].index)*0.5
val80_1 = len(tplist[5].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(20*len(dslist[5].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(50*len(dslist[5].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[5].loc[order0[round(80*len(dslist[5].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(20*len(tplist[5].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(50*len(tplist[5].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[5].loc[order1[round(80*len(tplist[5].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in late May -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 330, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-8, 330, 5)))
ax.set_yticklabels(np.linspace(0, 81, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 84, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 320)
ax2.set_xlim(min(ADAT0)-5, 320)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate173.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18183
order0=dslist[6].sort_values("ADAT").index
order1=tplist[6].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[6].index)+1):
    if dslist[6]['ADAT'][i] < 2016000:
        val = dslist[6]['ADAT'][i] - 2015000
    else:
        val = dslist[6]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[6].index)+1):
    if tplist[6]['ADAT'][i] < 2016000:
        val = tplist[6]['ADAT'][i] - 2015000
    else:
        val = tplist[6]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[6].index)*0.2
val50_0 = len(dslist[6].index)*0.5
val80_0 = len(dslist[6].index)*0.8
val20_1 = len(tplist[6].index)*0.2
val50_1 = len(tplist[6].index)*0.5
val80_1 = len(tplist[6].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(20*len(dslist[6].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(50*len(dslist[6].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[6].loc[order0[round(80*len(dslist[6].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(20*len(tplist[6].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(50*len(tplist[6].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[6].loc[order1[round(80*len(tplist[6].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in early July -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, 320, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-7, 330, 5)))
ax.set_yticklabels(np.linspace(0, 82, 7).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 7).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 320)
ax2.set_xlim(min(ADAT0)-5, 320)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate183.png", bbox_inches='tight')
plt.show()


#Anthesis date in 18193
order0=dslist[7].sort_values("ADAT").index
order1=tplist[7].sort_values("ADAT").index

fig = plt.figure(figsize=(10,10))
ax = fig.add_subplot(2,1,1)
ax2 = fig.add_subplot(2,1,2, sharex=ax)

ADAT0 = []
for i in range(1, len(dslist[7].index)+1):
    if dslist[7]['ADAT'][i] < 2016000:
        val = dslist[7]['ADAT'][i] - 2015000
    else:
        val = dslist[7]['ADAT'][i] - 2016000+365
    ADAT0.append(val)

ADAT1 = []
for i in range(1, len(tplist[7].index)+1):
    if tplist[7]['ADAT'][i] < 2016000:
        val = tplist[7]['ADAT'][i] - 2015000
    else:
        val = tplist[7]['ADAT'][i] - 2016000+365
    ADAT1.append(val)

val20_0 = len(dslist[7].index)*0.2
val50_0 = len(dslist[7].index)*0.5
val80_0 = len(dslist[7].index)*0.8
val20_1 = len(tplist[7].index)*0.2
val50_1 = len(tplist[7].index)*0.5
val80_1 = len(tplist[7].index)*0.8

ax.hist(np.asarray(ADAT0), bins=85, cumulative=True, color='red', histtype="barstacked")
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_0, val20_0], color="black", 
        label="20 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(20*len(dslist[7].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_0, val50_0], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(50*len(dslist[7].index)/100)],'ADAT']-2015000))
ax.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_0, val80_0], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(dslist[7].loc[order0[round(80*len(dslist[7].index)/100)],'ADAT']-2015000))
ax.legend(loc="best", fontsize=14)

ax2.hist(np.asarray(ADAT1), bins=85, cumulative=True, color='red', histtype="barstacked")
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val20_1, val20_1], color="black", 
        label="20 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(50*len(tplist[7].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val50_1, val50_1], color="blue", 
        label="50 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(50*len(tplist[7].index)/100)],'ADAT']-2015000))
ax2.plot([min(ADAT0)-10, max(ADAT0)+10],[val80_1, val80_1], color="orange", 
        label="80 percentile ADAT="+DOY2DATE(tplist[7].loc[order1[round(80*len(tplist[7].index)/100)],'ADAT']-2015000))
ax2.legend(loc="best", fontsize=14)

ax.set_title("The Cumulative Histogram of Anthesis date(Direct-sowing)", fontsize=18)
ax2.set_title("The Cumulative Histogram(Transplant) in middle July -Wgen-", fontsize=18)
ax2.set_xlabel("The Anthesis date of the simulation result(day)", fontsize=16)
ax.set_ylabel("cumulative percentage(%)", fontsize=16)
ax2.set_ylabel("cumulative percentage(%)", fontsize=16)
ax.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, 321, 5)))
ax2.set_xticklabels(doylist2Date(np.arange(min(ADAT0)-5, 321, 5)))
ax.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
ax2.set_yticklabels(np.linspace(0, 90, 5).astype(np.int32))
ax.set_xlim(min(ADAT0)-5, 325)
ax2.set_xlim(min(ADAT0)-5, 325)
plt.setp(ax.get_xticklabels(), fontsize=14, rotation=40, visible=False)
plt.setp(ax.get_yticklabels(), fontsize=14, visible=True)
plt.setp(ax2.get_xticklabels(), fontsize=14, rotation=40, visible=True)
plt.setp(ax2.get_yticklabels(), fontsize=14, visible=True)
#plt.savefig("190223_sskt_bcorrwgen_adat_png/190223_CDF_SSKT_WgenBcorr_Anthesis_pdate193.png", bbox_inches='tight')
plt.show()










































