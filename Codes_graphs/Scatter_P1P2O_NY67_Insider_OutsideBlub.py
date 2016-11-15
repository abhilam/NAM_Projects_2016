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

plt.scatter(Data_In['P1'],Data_In['P2O'],color='y')
plt.scatter(Data_Out['P1'],Data_Out['P2O'],color='r')
plt.legend(['Inside','Outside'],loc=4)
plt.xlabel('P1')
plt.ylabel('P2O')

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


plt.scatter(Data_In['P1'],Data_In['P2O'],color='y')
plt.scatter(Data_Out['P1'],Data_Out['P2O'],color='r')
plt.legend(['Inside','Outside'],loc=4)
plt.xlabel('P1')
plt.ylabel('P2O')

plt.show()
