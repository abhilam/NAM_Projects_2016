# -*- coding: utf-8 -*-
"""
Created on Mon Aug 29 09:25:52 2016

@author: abhi

Email: abhilam@ksu.edu
Purpose:


Kansas State University
Manhattan, KS

"""

import pandas as pd
from os import listdir
import matplotlib.pylab as plt
import numpy as np
import os

import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')
def rnd(x):
    return round(x,5)
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Check_Optimization/')

Data_In=pd.read_csv('DE_NY67_DataInside.csv',sep=',',skiprows=0,header=0)
Data_In=Data_In[Data_In['Pop_No']<28]#.reset_index()
Data_Out=pd.read_csv('DE_NY67_DataOutside.csv',sep=',',skiprows=0,header=0)
Data_Out=Data_Out[Data_Out['Pop_No']<28]#.reset_index()

plt.scatter(Data_In['P2O'],Data_In['P1'],color='y')
plt.scatter(Data_Out['P2O'],Data_Out['P1'],color='r')
plt.legend(['Expressible','InExpressible'],loc=4)
plt.ylabel('P1')
plt.xlabel('P2O')

plt.show()

############### Plot P1_P2 for NY67_SOBOL
path='/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/'
Data=pd.read_csv(path+'Output_4Parms_NAM_NY6NY7.csv',sep=',',skiprows=0,header=0)
plt.figure(2)
plt.scatter(Data['P1'],Data['P2O'])
plt.xlabel('P1');plt.ylabel('P2O')
plt.show()

plt.figure(3)
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/ConvexHull/')
Data_In=pd.read_csv('Sobol_NY67_DataInside.csv',sep=',',skiprows=0,header=0)
Data_In=Data_In[Data_In['Pop_No']<28]#.reset_index()

Data_Out=pd.read_csv('Sobol_NY67_DataOutside.csv',sep=',',skiprows=0,header=0)
Data_Out=Data_Out[Data_Out['Pop_No']<28]#.reset_index()

DatIn_250_55=len(Data_In[(Data_In['P1']>245)& (Data_In['P1']<260)])
#DatIn_236_40=len(Data_In[(Data_In['P1']>236)& (Data_In['P1']<240)])

DatOut_250_55=len(Data_Out[(Data_Out['P1']>245)& (Data_Out['P1']<260)])
DatOut_236_40=len(Data_Out[(Data_Out['P1']>236)& (Data_Out['P1']<240)])
plt.ylim(50,400)
plt.xlim(4,22)
plt.scatter(Data_In['P2O'],Data_In['P1'],color='y')
plt.scatter(Data_Out['P2O'],Data_Out['P1'],color='r')
plt.legend(['Expressible','InExpressible'],loc=4)
plt.ylabel('P1')
plt.xlabel('P2O')

plt.show()

plt.figure(4)
path='/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/'
Data=pd.read_csv(path+'Output_4Parms_NAM_NY6NY7.csv',sep=',',skiprows=0,header=0)
plt.scatter(Data['P2O'],Data['P1'],color='b')
plt.xlabel('P2O')
plt.ylabel('P1')
plt.title('NY6-NY7')
plt.show()

