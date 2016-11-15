# -*- coding: utf-8 -*-
"""
Created on Wed Aug  3 12:01:01 2016

@author: abhi

Email: abhilam@ksu.edu
Purpose:


Kansas State University
Manhattan, KS

"""
import matplotlib.pyplot as mpl
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/')
mpl.rcParams['font.size'] = 20
mpl.rc('font', family='sans-serif')
Site=['NY06','NY07','NC06','NC07','MOC06','MOC07','ILV06','ILV07','FLH06','FLH07','PRT06']

Data=pd.read_csv('Output_4Parms_NAM.csv',sep=',',skiprows=0,header=0)
Data=Data[Data['Pop_No']<28].reset_index()
Data3SY=pd.read_csv('Output_4Parms_NAM_FLPR.csv',sep=',',skiprows=0,header=0)
Data3SY=Data3SY[Data3SY['Pop_No']<28].reset_index()

Data8SY=pd.read_csv('Output_4Parms_NAM_No_FLPR.csv',sep=',',skiprows=0,header=0)
Data8SY=Data8SY[Data8SY['Pop_No']<28].reset_index()

plt.figure(1)
ax=plt.subplot(241)

plt.scatter(Data['P2O'],Data['Phint'])
plt.ylabel('PHINT')
plt.xlim(10,14);plt.ylim(22,77)
ax.set_xticklabels([])


ax=plt.subplot(242)
plt.scatter(Data8SY['P2O'],Data8SY['Phint'])
#plt.xlabel('P2O');#plt.ylabel('PHINT')
plt.xlim(10,14);plt.ylim(22,77)
ax.set_xticklabels([]);ax.set_yticklabels([])

ax=plt.subplot(243)
plt.scatter(Data3SY['P2O'],Data3SY['Phint'])
#plt.xlabel('P2O');#plt.ylabel('PHINT')
plt.xlim(10,14);plt.ylim(22,77)
ax.set_xticklabels([]);ax.set_yticklabels([])

ax=plt.subplot(245)
for i in xrange(11):
    #val=Data[Data['OSite'+str(i+1)]>-99].reset_index(drop=0)
    val=Data
    P2O=np.sort(val['P2O'])
    p=1.* np.arange(len(P2O))/(len(P2O)-1)
    plt.plot(P2O,p,'-b',linewidth=2,label=Site[i+0])
    #plt.legend(loc=2,ncol=2)
    plt.ylabel('Probability')
    plt.xlabel('P2O');
    Mjtck=np.arange(10,15,1)
    ax.set_xticks(Mjtck)
plt.xticks(rotation=90)

ax=plt.subplot(246)
for i in xrange(8):
    #val=Data8SY[Data8SY['OSite'+str(i+1)]>-99].reset_index(drop=0)
    val=Data8SY
    P2O=np.sort(val['P2O'])
    p=1.* np.arange(len(P2O))/(len(P2O)-1)
    plt.plot(P2O,p,'-b',linewidth=2,label=Site[i+0],)
    #plt.legend(loc=2,ncol=2)
    #plt.ylabel('Probability')
    plt.xlabel('P2O');ax.set_yticklabels([])
    Mjtck=np.arange(10,15,1)
    ax.set_xticks(Mjtck)
plt.xticks(rotation=90)

ax=plt.subplot(247)
for i in xrange(3):
    #val=Data3SY[Data3SY['OSite'+str(i+9)]>-99].reset_index(drop=0)
    val=Data3SY
    P2O=np.sort(val['P2O'])
    p=1.* np.arange(len(P2O))/(len(P2O)-1)
    plt.plot(P2O,p,'-b',linewidth=2,label=Site[i+8])
    #plt.legend(loc=4)
    #plt.ylabel('Probability')
    plt.xlabel('P2O')
    ax.set_yticklabels([])
    Mjtck=np.arange(10,15,1)
    ax.set_xticks(Mjtck)
plt.xticks(rotation=90)


# Plot Scatter DE FLPR67
path='/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Codes_NAM/'
Data2=pd.read_csv(path+'DE_SOBOL_Parms_FL67PR6.csv',sep=',',skiprows=1,header=0)
Data2=Data2[Data2['Pop_No']<28].reset_index()
ax=plt.subplot(244)
plt.scatter(Data2['P2O_DE'],Data2['Phint_DE'])
ax.set_xticklabels([]);ax.set_yticklabels([])

ax=plt.subplot(248)
P2O=np.sort(Data2['P2O_DE'])
p=1.* np.arange(len(P2O))/(len(P2O)-1)
plt.plot(P2O,p,'-b',linewidth=2,label=Site[i+8])
#plt.legend(loc=4)
#plt.ylabel('Probability')
plt.xlabel('P2O')
ax.set_yticklabels([])
Mjtck=np.arange(6,22,2)
ax.set_xticks(Mjtck)
plt.xticks(rotation=90)


plt.show()
plt.tight_layout()
