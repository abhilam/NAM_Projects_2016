# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 10:29:11 2016

@author: abhi

Email: abhilam@ksu.edu
Purpose:


Kansas State University
Manhattan, KS

"""
import pandas as pd
import numpy as np
import matplotlib.pylab as plt
from math import *
import os
import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Cont_Table/')
Path='/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/'#'/home/abhi/Desktop/NAME_MAIZE/'
Data=pd.read_csv(Path+'Output_4Parms_NAM_NY6NY7.csv', sep=',',skiprows=0,header=0)


Data=Data[(Data['OSite1']>0)& (Data['OSite2']>0)].reset_index(drop=0)
Data=Data[Data['Pop_No']<28].reset_index(drop=0) # This is to remove Pop 28

#Data=Data[(Data['MSite1']==87)& (Data['MSite2']==78)& (Data['No_Sim']==2)].reset_index(drop=0)
DataRange=pd.read_csv(Path+'NAM_Output_NY67_Equifinality_Range_2.csv',sep=',',skiprows=0,header=0)

DataRange=DataRange[DataRange['Pop_No']<28].reset_index(drop=0) # This is to remove Pop 28

P1Range=[]
P2Range=[]
P2ORange=[]
PhintRange=[]



for i in xrange(len(Data)):
    val=DataRange[(DataRange['Pop_No']==Data['Pop_No'][i])& (DataRange['Line_No']==Data['Line_No'][i])].reset_index(drop=0)
    P1Range.append(((val['P1max'][0]-val['P1min'][0])*200)/(val['P1max'][0]+val['P1min'][0]))
    P2Range.append(((val['P2max'][0]-val['P2min'][0])*4*200)/(val['P2max'][0]+val['P2min'][0]))
    P2ORange.append(((val['P2Omax'][0]-val['P2Omin'][0])*4*200)/(val['P2Omax'][0]+val['P2Omin'][0]))
    PhintRange.append(((val['Phintmax'][0]-val['Phintmin'][0])*4*200)/(val['Phintmax'][0]+val['Phintmin'][0]))



equifinality_log=[log10(x) for x in Data['No_Tie']]
#for i in xrange(len(Data['MSite1'])):
plt.figure(1)
#plt.subplot(221)

plt.scatter(Data['MSite1'],Data['MSite2'],c=equifinality_log,s=P1Range,cmap=plt.cm.jet)
plt.colorbar()
plt.xlabel('Anthesis Days (NY6)')
#plt.tight_layout()
plt.ylabel('Anthesis Days (NY7)')
plt.show()
plt.figure(2)
#ax=plt.subplot(222)
#Data=Data[(Data['OSite1']>0)& (Data['OSite2']>0)].reset_index(drop=0)
equifinality_log=[log10(x) for x in Data['No_Tie']]
plt.scatter(Data['OSite1'],Data['OSite2'],c=equifinality_log,s=P1Range,cmap=plt.cm.jet)
plt.colorbar()
plt.xlabel('Anthesis Days (NY6)')
#ax.set_yticklabels([])
plt.ylabel('Anthesis Days (NY7)')
plt.show()
