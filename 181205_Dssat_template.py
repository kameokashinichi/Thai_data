#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  5 11:32:20 2018

@author: kameokashinichi
"""


"""
181205 generate experimental file for Dssat

1. Define the format of experimental file(refer to index.js)
reference url -> https://note.nkmk.me/python-format-zero-hex/
reference url2(str.template) -> https://ja.stackoverflow.com/questions/41222/python%E3%81%A7-%E9%9B%9B%E5%BD%A2%E3%82%92%E4%BD%BF%E3%81%A3%E3%81%A6%E3%83%86%E3%82%AD%E3%82%B9%E3%83%88%E3%83%95%E3%82%A1%E3%82%A4%E3%83%AB%E3%81%B8%E5%87%BA%E5%8A%9B%E3%81%97%E3%81%9F%E3%81%84

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
import sys


#generate template for each section

def getHeader(detail, adress, site):
    header = """
*EXP.DETAILS:{detail}

*GENERAL
@PEOPLE
-99
@ADDRESS
{adress}
@SITE
{site}
@ PAREA  PRNO  PLEN  PLDR  PLSP  PLAY HAREA  HRNO  HLEN  HARM.........
    -99   -99   -99   -99   -99   -99   -99   -99   -99   -99
    """.format(detail=detail, adress=adress, site=site)
    
    return header

def getTreatmentHeader():
    TH = """
*TREATMENTS                        -------------FACTOR LEVELS------------
@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM\
    """
    
    return TH



#Treatment section

def generate_Tnum(n, tname, cu, fl, ic, mp, mi, mf, mr, sm, r=1, o=0, c=0, sa=0, mc=0, mt=0, me=0, mh=0):
    """
    n    : int
        the serial number of the treatment
    tname: str
        the name of the treatment
    cu   : int
        the serial number of the cultivar
    fl   : int
        the serial number of the field
    ic   : int
        the serial number of the initial conditions
    mp   : int
        the serial number of planting details
    mi   : int
        the serial number of irrigation
    mf   : int
        the serial number of fertilizer(inorganic)
    mr   : int
        the serial number of organic materials
    sm   : int
        the serial number of simulation controls
    """
    Tnum = """
%2.0f%2.0f%2.0f%2.0f %-25s%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f%3.0f\
    """
    
    Tnum = Tnum % (n, r, o, c, tname, cu, fl, sa, ic, mp, mi, mf, mr, mc, mt, me, mh, sm)

    #path_w = os.getcwd()+'/test.txt'
    
    #with open(path_w, mode='a') as f:
        #f.write(Tnum)
    print(Tnum)
    
    return Tnum

def generate_multi_Tnum(n, cu, fl, ic, mp, mi, mf, mr, sm):
    
    if n>99:
        print("Error: the number of simulation must be less than 100")
    
    elif n==cu or n==fl or n==ic or n==mp or n==mi or n==mf or n==mr or n==sm:
        cuarr=np.tile(np.arange(1, cu+1), int(12/np.arange(1, cu+1)))
        flarr=np.tile(np.arange(1, fl+1), int(12/np.arange(1, fl+1)))
        icarr=np.tile(np.arange(1, ic+1), int(12/np.arange(1, ic+1)))
        mparr=np.tile(np.arange(1, mp+1), int(12/np.arange(1, mp+1)))
        miarr=np.tile(np.arange(1, mi+1), int(12/np.arange(1, mi+1)))
        mfarr=np.tile(np.arange(1, mf+1), int(12/np.arange(1, mf+1)))
        mrarr=np.tile(np.arange(1, mr+1), int(12/np.arange(1, mr+1)))
        smarr=np.tile(np.arange(1, sm+1), int(12/np.arange(1, sm+1)))
        
        Tnum = ""
        for i in range(1, n+1):
            Tnum = Tnum + generate_Tnum(n=i, tname=repr(i), cu=cuarr[i], fl=flarr[i], ic=icarr[i], mp=mparr[i], mi=miarr[i], 
                          mf=mfarr[i], mr=mrarr[i], sm=smarr[i], r=1, o=0, c=0, sa=0, mc=0, mt=0, me=0, mh=0)
            
    else:
        if n != cu*fl*ic*mp*mi*mf*mr*sm:
            print("Error : setting of the number of simulation cannot fulfill all combinations")
        else:
            cua = np.arange(1, cu+1)
            fla = np.arange(1, fl+1)
            ica = np.arange(1, ic+1)
            mpa = np.arange(1, mp+1)
            mia = np.arange(1, mi+1)
            mfa = np.arange(1, mf+1)
            mra = np.arange(1, mr+1)
            sma = np.arange(1, sm+1)
            cum, flm, icm, mpm, mim, mfm, mrm, smm = np.meshgrid(cua, fla, ica, mpa, mia, mfa, mra, sma)
            Tnum = ""
            m = 1
            for i in range(n):   #use ndarray.item function
                Tnum = Tnum + generate_Tnum(i+1, repr(m), cum.item(i), flm.item(i), icm.item(i), mpm.item(i), 
                                          mim.item(i), mfm.item(i), mrm.item(i), smm.item(i), r=1, o=0, 
                                          c=0, sa=0, mc=0, mt=0, me=0, mh=0)
                m=m+1
    return Tnum




#CU "Cultivar" Section

        
def generateCultivarHeader():
    culHeader = """\n
*CULTIVARS
@C CR INGENO CNAME\
"""
    return culHeader

def generateCulNum(c, specie, code, variety):
    """
    c      : int
        the serial number of the targeted specie
    specie : str
        the ICASA code of the crop specie (Rice->'RI', Cabbage->'CB' etc)
    code   : str
        the dssat code of each variety
    variety: str
        the variety name resistered in .CUL file
        
    """
    
    cNum = """
%2.0f%3s%7s %-10s\
"""
    cNum = cNum % (c, specie, code, variety)

    return cNum

def generateMulti_CulNum(c, specie, code, variety):
    """
    c      : list(int)
        the serial number of the targeted specie
    specie : list(str)
        the ICASA code of the crop specie (Rice->'RI', Cabbage->'CB' etc)
    code   : list(str)
        the dssat code of each variety
    variety: list(str)
        the variety name resistered in .CUL file
    """    
    if len(c) != len(specie) != len(code) != len(variety):
        print("Error: the size of the input variables must be same")
        sys.exit()
    
    else:
        cNum = ''
        for i in range(len(c)):
            cNum = cNum + generateCulNum(c[i], specie[i], code[i], variety[i])
            
        return cNum



# FL "Field" section
    
def generateFieldHeader():

    fheader = """\n    
*FIELDS
@L ID_FIELD WSTA....  FLSA  FLOB  FLDT  FLDD  FLDS  FLST SLTX  SLDP  ID_SOIL    FLNAME\
    """
    
    return fheader

def generateFieldNum(l, id_f, wsta, sldp, id_soil, flsa=-99, flob=0, fldt='DR000', fldd=0, flds=0,
                     flst=00000, sltx=-99, flname=-99):
    """
    l      : int
        the serial number of the field .
    id_f   : str
        the name of the condition.
    wsta   : str
        the name of the weather file(.WTH) stored in Dssat.
    sldp   : int
        the depth of the cultured soil(cm).
    id_soil: str
        the ID of the soil texture stored in Dssat.
    """
    
    fNum = """
%2.0f %-8s %-8s%6.0f%6.0f%6s%6.0f%6.0f%6.0f %-4.0f%6.0f  %-11s%-8s\
"""
    fNum = fNum % (l, id_f, wsta, flsa, flob, fldt, fldd, flds, flst, sltx, sldp, id_soil, flname)
    
    return fNum

def generateMultiFNum(l, id_f, wsta, sldp, id_soil):
    """
    l      : list(int)
        the list of the serial number of the field .
    id_f   : list(str)
        the list of the name of the condition.
    wsta   : list(str)
        the list of the name of the weather file(.WTH) stored in Dssat.
    sldp   : list(int)
        the list of the depth of the cultured soil(cm).
    id_soil: list(str)
        the list of the ID of the soil texture stored in Dssat.
    """
    
    fNum = ""
    for i in range(len(l)):
        fNum = fNum + generateFieldNum(l[i], id_f[i], wsta[i], sldp[i], id_soil[i], 
                                       flsa=-99, flob=0, fldt='DR000', fldd=0, flds=0,
                                       flst=00000, sltx=-99, flname=-99)
    
    return fNum
    

# "IC", Initial conditions
def getICHeader_1():
    ich_1 = """
*INITIAL CONDITIONS
@C   PCR ICDAT  ICRT  ICND  ICRN  ICRE  ICWD ICRES ICREN ICREP ICRIP ICRID ICNAME\
"""
    return ich_1

def getICHeader_2():
    ich_2 = """
@C  ICBL  SH2O  SNH4  SNO3\
"""

def generateICNum_1(c, pcr, icdat, icrt, icrn, icre, icrip, icrid, icnd=-99, icwd=-99, icres=-99, icren=-99, icrep=-99, icname=-99):
    """
    c    : int
        the serial number of initial condition menu
    pcr  : str
        the ICASA code of the variety which was planted before
    icdat: int
        the year and date of the initial condition measured(yydoy)
    icrt : int
        root weight from previous crop(kg/ha)
    icrn : int
        rhizobia number(0 or 1)
    icre : int
        rhizobia effectiveness(0 or 1)
    icrip: int
        initial residue incorporation(%)
    icrid
    """
    icNum_1 = """
%2.0f   %3s %5.0f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f%6.0f %-15s\
"""
    icNum_1 = icNum_1 % (c, pcr, icdat, icrt, icnd, icrn, icre, icwd, icres, icren, icrep, icrip, icrid, icname)

    return icNum_1

def generateICNum_2(c, icbl, sh2o, snh4, sno3):
    """
    c   : int
        the serial number of the initial conditions
    icbl: int
        the depth of the soil condition(cm)
    sh2o: str
        the water content of soil in the layer(volmetric ratio cm3/cm3)
    snh4: str
        the NH4 content of soil in the layer(ppm)
    sno3: str
        the NO3 contentof soil in the layer(ppm)
    """
    icNum_2 = """
%2.0f%6.0f%6.0s%6.0s%6.0s\
"""
    icNum_2 % (c, icbl, sh2o, snh4, sno3)
    
    return icNum

def genMultiICNum_2(c, icbl, sh2o, snh4, sno3):
    """
    c   : int
        the serial number of the initial conditions
    icbl: list(int)
        the depth of the soil condition(cm)
    sh2o: list(str)
        the water content of soil in the layer(volmetric ratio cm3/cm3)
    snh4: list(str)
        the NH4 content of soil in the layer(ppm)
    sno3: list(str)
        the NO3 contentof soil in the layer(ppm)
    """
    inNum_2 = ""
    for i in range(len(icbl)):
        generateICNum_2(c, icbl[i], sh2o[i], snh4[i], sno3[i])


def generateICNum_2_multi():


def writeTemplate(detail, adress, site, n, cu, fl, ic, mp, mi, mf, mr, sm, c, specie, code, variety, l, id_f, wsta, sldp, id_soil):
    
    temp = getHeader(detail, adress, site)+getTreatmentHeader()+\
    generate_multi_Tnum(n, cu, fl, ic, mp, mi, mf, mr, sm)+\
    generateCultivarHeader()+generateMulti_CulNum(c, specie, code, variety)+\
    generateFieldHeader()+generateMultiFNum(l, id_f, wsta, sldp, id_soil)
    
    with open('test.txt', 'w') as f:
        f.write(temp)



