# -*- coding: utf-8 -*-
"""
Created on Thu Aug 25 09:54:38 2016

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

import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')

os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Codes_NAM/')
Data=pd.read_csv('DE_SOBOL_Parms_FL67PR6.csv', sep=',',skiprows=1,header=0)
Data=Data[Data['Pop_No']<28].reset_index()
ADATIndex=[]
FL6=np.mean([x for x in Data['OSite9'] if x>0])
FL7=np.mean([x for x in Data['OSite10'] if x>0])
PR6=np.mean([x for x in Data['OSite11'] if x>0])
Mean=[FL6,FL7,PR6]
for i in xrange(len(Data)):
    val1=Data.iloc[i]
    adat=[val1['OSite9'],val1['OSite10'],val1['OSite11']]
    adat1=[x for x in adat if x>0]
    if len(adat)>0:
        ADATIndex.append(sum([adat[i]-Mean[i] for i in xrange(len(adat)) if adat[i]>0])/len(adat1))

#ADATIndex=[]# weighted index of ADAT
#for i in xrange(len(Data)):
#    val1=Data.iloc[i]
#    adat=[val1['OSite9'],val1['OSite10'],val1['OSite11']]
#    adat=[x for x in adat if x>0]
#    if len(adat)>0:
#        ADATIndex.append(sum(abs(np.array(adat)-np.mean(adat))))

mxadat=[max([Data['OSite9'][i],Data['OSite10'][i],Data['OSite11'][i]]) for i in xrange(len(Data))]
fig=plt.figure(1)
plt.subplot(2,3,1)
plt.scatter(Data['RMSE_Sob'],Data['RMSE_DE'],c=mxadat)
plt.xlabel('Sobol RMSE');plt.ylabel('DE RMSE')
plt.subplot(2,3,2)
plt.scatter(Data['P1_Sob'],Data['P1_DE'],c=mxadat)
plt.xlabel('Sobol P1');plt.ylabel('DE P1')
plt.subplot(2,3,3)
plt.scatter(Data['P2_Sob'],Data['P2_DE'],c=mxadat)
plt.xlabel('Sobol P2');plt.ylabel('DE P2')
plt.subplot(2,3,4)
plt.scatter(Data['Phint_Sob'],Data['Phint_DE'],c=mxadat)
plt.xlabel('Sobol Phint');plt.ylabel('DE Phint')
plt.subplot(2,3,5)
plt.scatter(Data['P2O_Sob'],Data['P2O_DE'],c=mxadat)
plt.xlabel('Sobol P2O');plt.ylabel('DE P2O')
plt.colorbar()
plt.subplot(2,3,6)
plt.scatter(Data['Phint_Sob'],Data['Phint_DE'],c=Data['P2O_Sob'])
plt.xlabel('Sobol Phint');plt.ylabel('DE Phint')
plt.colorbar()
plt.show()


######################### GRAPH based on diff RMSE to diff parameter
fig=plt.figure(2)
#mxadat=Data['No_Tie']
abc=Data['RMSE_Sob']-Data['RMSE_DE']
print 'greater then 0',len([item for item in abc if item >0])
print 'less then 0',len([item for item in abc if item <0])
print 'Total=',len([item for item in abc if item ==0])

plt.subplot(2,2,1)
plt.scatter(Data['RMSE_Sob']-Data['RMSE_DE'],Data['P1_Sob']-Data['P1_DE'],c=mxadat)
D={'rmse':Data['RMSE_Sob']-Data['RMSE_DE'],'P1':Data['P1_Sob']-Data['P1_DE']}
df=pd.DataFrame(D)
LUQ1=len(df[(df['rmse']<0)&(df['P1']>0)])
LLQ1=len(df[(df['rmse']<0)&(df['P1']<0)])
RUQ1=len(df[(df['rmse']>0)&(df['P1']>0)])
RLQ1=len(df[(df['rmse']>0)&(df['P1']<0)])

LC1=len(df[(df['rmse']<0)&(df['P1']==0)])
RC1=len(df[(df['rmse']>0)&(df['P1']==0)])
UC1=len(df[(df['rmse']==0)&(df['P1']>0)])
LoC1=len(df[(df['rmse']==0)&(df['P1']<0)])
plt.text(-1.25,0,str(LC1));plt.text(0.75,0,str(RC1));plt.text(0,300,str(UC1));plt.text(0,-150,str(LoC1));
plt.text(-1.25,300,str(LUQ1));plt.text(-1.25,-150,str(LLQ1));plt.text(0.75,300,str(RUQ1));plt.text(0.75,-150,str(RLQ1));
plt.axvline(x=0);plt.axhline(y=0)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P1-DE P1')

plt.subplot(2,2,2)
plt.scatter(Data['RMSE_Sob']-Data['RMSE_DE'],Data['P2_Sob']-Data['P2_DE'],c=mxadat)
D={'rmse':Data['RMSE_Sob']-Data['RMSE_DE'],'P2':Data['P2_Sob']-Data['P2_DE']}
df=pd.DataFrame(D)
LUQ2=len(df[(df['rmse']<0)&(df['P2']>0)])
LLQ2=len(df[(df['rmse']<0)&(df['P2']<0)])
RUQ2=len(df[(df['rmse']>0)&(df['P2']>0)])
RLQ2=len(df[(df['rmse']>0)&(df['P2']<0)])

LC2=len(df[(df['rmse']<0)&(df['P2']==0)])
RC2=len(df[(df['rmse']>0)&(df['P2']==0)])
UC2=len(df[(df['rmse']==0)&(df['P2']>0)])
LoC2=len(df[(df['rmse']==0)&(df['P2']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC2));plt.text(0.75,0,str(RC2));plt.text(0,2,str(UC2));plt.text(0,-6,str(LoC2));
plt.text(-1.25,2,str(LUQ2));plt.text(-1.25,-6,str(LLQ2));plt.text(0.75,2,str(RUQ2));plt.text(0.75,-6,str(RLQ2));

plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2-DE P2')

plt.subplot(2,2,3)
plt.scatter(Data['RMSE_Sob']-Data['RMSE_DE'],Data['Phint_Sob']-Data['Phint_DE'],c=mxadat)
D={'rmse':Data['RMSE_Sob']-Data['RMSE_DE'],'Phint':Data['Phint_Sob']-Data['Phint_DE']}
df=pd.DataFrame(D)
LUQ3=len(df[(df['rmse']<0)&(df['Phint']>0)])
LLQ3=len(df[(df['rmse']<0)&(df['Phint']<0)])
RUQ3=len(df[(df['rmse']>0)&(df['Phint']>0)])
RLQ3=len(df[(df['rmse']>0)&(df['Phint']<0)])

LC3=len(df[(df['rmse']<0)&(df['Phint']==0)])
RC3=len(df[(df['rmse']>0)&(df['Phint']==0)])
UC3=len(df[(df['rmse']==0)&(df['Phint']>0)])
LoC3=len(df[(df['rmse']==0)&(df['Phint']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC3));plt.text(0.75,0,str(RC3));plt.text(0,40,str(UC3));plt.text(0,-100,str(LoC3));
plt.text(-1.25,40,str(LUQ3));plt.text(-1.25,-100,str(LLQ3));plt.text(0.75,40,str(RUQ3));plt.text(0.75,-100,str(RLQ3));


plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol Phint-DE Phint')

plt.subplot(2,2,4)
plt.scatter(Data['RMSE_Sob']-Data['RMSE_DE'],Data['P2O_Sob']-Data['P2O_DE'],c=mxadat)
D={'rmse':Data['RMSE_Sob']-Data['RMSE_DE'],'P2O':Data['P2O_Sob']-Data['P2O_DE']}
df=pd.DataFrame(D)
LUQ4=len(df[(df['rmse']<0)&(df['P2O']>0)])
LLQ4=len(df[(df['rmse']<0)&(df['P2O']<0)])
RUQ4=len(df[(df['rmse']>0)&(df['P2O']>0)])
RLQ4=len(df[(df['rmse']>0)&(df['P2O']<0)])

LC4=len(df[(df['rmse']<0)&(df['P2O']==0)])
RC4=len(df[(df['rmse']>0)&(df['P2O']==0)])
UC4=len(df[(df['rmse']==0)&(df['P2O']>0)])
LoC4=len(df[(df['rmse']==0)&(df['P2O']<0)])

plt.axvline(x=0);plt.axhline(y=0)
plt.text(-1.25,0,str(LC4));plt.text(0.75,0,str(RC4));plt.text(0,7,str(UC4));plt.text(0,-12,str(LoC4));
plt.text(-1.25,7,str(LUQ4));plt.text(-1.25,-12,str(LLQ4));plt.text(0.75,7,str(RUQ4));plt.text(0.75,-12,str(RLQ4));
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2O-DE P2O')

plt.colorbar()

plt.show()

################################### SECOND GRAPH based on P2O Change Category
#NewData=pd.DataFrame()
fig=plt.figure(3)

NewData=pd.DataFrame()
for i in xrange(len(Data)):
    if (Data['P2O_Sob'][i]<12) & (Data['P2O_DE'][i]<12):
        NewData=NewData.append(Data.iloc[i])
plt.subplot(2,2,1)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P1_Sob']-NewData['P1_DE'],color='y',s=2)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P1-DE P1')
plt.text(-1.25,0,str(LC1));plt.text(0.75,0,str(RC1));plt.text(0,300,str(UC1));plt.text(0,-150,str(LoC1));
plt.text(-1.25,300,str(LUQ1));plt.text(-1.25,-150,str(LLQ1));plt.text(0.75,300,str(RUQ1));plt.text(0.75,-150,str(RLQ1));
plt.axvline(x=0);plt.axhline(y=0)
plt.text(-1.5,350,'P2O<12SB=>P2O<12DE: '+str(len(NewData)),color='y')
plt.subplot(2,2,2)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2_Sob']-NewData['P2_DE'],color='y',s=2)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2-DE P2')
plt.axvline(x=0);plt.axhline(y=0)
plt.text(-1.25,0,str(LC2));plt.text(0.75,0,str(RC2));plt.text(0,2,str(UC2));plt.text(0,-6,str(LoC2));
plt.text(-1.25,2,str(LUQ2));plt.text(-1.25,-6,str(LLQ2));plt.text(0.75,2,str(RUQ2));plt.text(0.75,-6,str(RLQ2));
plt.subplot(2,2,3)
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC3));plt.text(0.75,0,str(RC3));plt.text(0,40,str(UC3));plt.text(0,-100,str(LoC3));
plt.text(-1.25,40,str(LUQ3));plt.text(-1.25,-100,str(LLQ3));plt.text(0.75,40,str(RUQ3));plt.text(0.75,-100,str(RLQ3));

plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['Phint_Sob']-NewData['Phint_DE'],color='y',s=2)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol Phint-DE Phint')
plt.subplot(2,2,4)
plt.axvline(x=0);plt.axhline(y=0)
plt.text(-1.25,0,str(LC4));plt.text(0.75,0,str(RC4));plt.text(0,7,str(UC4));plt.text(0,-12,str(LoC4));
plt.text(-1.25,7,str(LUQ4));plt.text(-1.25,-12,str(LLQ4));plt.text(0.75,7,str(RUQ4));plt.text(0.75,-12,str(RLQ4));
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2O_Sob']-NewData['P2O_DE'],color='y',s=2)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2O-DE P2O')


NewData=pd.DataFrame()
for i in xrange(len(Data)):
    if (Data['P2O_Sob'][i]>12) & (Data['P2O_DE'][i]>12):
        NewData=NewData.append(Data.iloc[i])
plt.subplot(2,2,1)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P1_Sob']-NewData['P1_DE'],color='r',s=2)
plt.text(-1.5,320,'P2O>12SB=>P2O>12DE: '+str(len(NewData)),color='r')
plt.subplot(2,2,2)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2_Sob']-NewData['P2_DE'],color='r',s=2)
plt.subplot(2,2,3)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['Phint_Sob']-NewData['Phint_DE'],color='r',s=2)
plt.subplot(2,2,4)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2O_Sob']-NewData['P2O_DE'],color='r',s=2)

NewData=pd.DataFrame()
for i in xrange(len(Data)):
    if (Data['P2O_Sob'][i]<12) & (Data['P2O_DE'][i]>12):
        NewData=NewData.append(Data.iloc[i])
plt.subplot(2,2,1)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P1_Sob']-NewData['P1_DE'],color='royalblue',s=2)
plt.text(-1.5,375,'P2O<12SB=>P2O>12DE: '+str(len(NewData)),color='b')
plt.subplot(2,2,2)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2_Sob']-NewData['P2_DE'],color='royalblue',s=2)
plt.subplot(2,2,3)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['Phint_Sob']-NewData['Phint_DE'],color='royalblue',s=2)
plt.subplot(2,2,4)
plt.scatter(NewData['RMSE_Sob']-NewData['RMSE_DE'],NewData['P2O_Sob']-NewData['P2O_DE'],color='royalblue',s=2)


######################## PLot Data Scatter based on weighted Index Data Sorted by weighted Index

mxadat=ADATIndex
Data1=Data
Data1['ADATIndex']=ADATIndex
Data1=Data1.sort(['ADATIndex'])
wtIndex=Data1['ADATIndex']
fig=plt.figure(4)
plt.subplot(2,3,1)
plt.scatter(Data1['RMSE_Sob'],Data1['RMSE_DE'],c=wtIndex)
plt.xlabel('Sobol RMSE');plt.ylabel('DE RMSE')
plt.subplot(2,3,2)
plt.scatter(Data1['P1_Sob'],Data1['P1_DE'],c=wtIndex)
plt.xlabel('Sobol P1');plt.ylabel('DE P1')
plt.subplot(2,3,3)
plt.scatter(Data1['P2_Sob'],Data1['P2_DE'],c=wtIndex)
plt.xlabel('Sobol P2');plt.ylabel('DE P2')
plt.subplot(2,3,4)
plt.scatter(Data1['Phint_Sob'],Data1['Phint_DE'],c=wtIndex)
plt.xlabel('Sobol Phint');plt.ylabel('DE Phint')
plt.subplot(2,3,5)
plt.scatter(Data1['P2O_Sob'],Data1['P2O_DE'],c=wtIndex)
plt.xlabel('Sobol P2O');plt.ylabel('DE P2O')
plt.colorbar()
plt.subplot(2,3,6)
plt.scatter(Data1['Phint_Sob'],Data1['Phint_DE'],c=Data['P2O_Sob'])
plt.xlabel('Sobol Phint');plt.ylabel('DE Phint')
plt.colorbar()
plt.show()


##########################################
######################### GRAPH based on diff RMSE to diff parameter color by weighted index and data sorted by weighted index
fig=plt.figure(5)
#mxadat=Data['No_Tie']
abc=Data['RMSE_Sob']-Data['RMSE_DE']
print 'greater then 0',len([item for item in abc if item >0])
print 'less then 0',len([item for item in abc if item <0])
print 'Total=',len([item for item in abc if item ==0])
Data2=Data
Data2['ADATIndex']=ADATIndex
Data2=Data1.sort(['ADATIndex'])
wtIndex=Data2['ADATIndex']

plt.subplot(2,2,1)

plt.scatter(Data2['RMSE_Sob']-Data2['RMSE_DE'],Data2['P1_Sob']-Data2['P1_DE'],c=wtIndex)
D={'rmse':Data2['RMSE_Sob']-Data2['RMSE_DE'],'P1':Data2['P1_Sob']-Data2['P1_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P1']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P1']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P1']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P1']<0)])

LC=len(df[(df['rmse']<0)&(df['P1']==0)])
RC=len(df[(df['rmse']>0)&(df['P1']==0)])
UC=len(df[(df['rmse']==0)&(df['P1']>0)])
LoC=len(df[(df['rmse']==0)&(df['P1']<0)])
plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,300,str(UC));plt.text(0,-150,str(LoC));
plt.text(-1.25,300,str(LUQ));plt.text(-1.25,-150,str(LLQ));plt.text(0.75,300,str(RUQ));plt.text(0.75,-150,str(RLQ));
plt.axvline(x=0);plt.axhline(y=0)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P1-DE P1')

plt.subplot(2,2,2)
plt.scatter(Data2['RMSE_Sob']-Data2['RMSE_DE'],Data2['P2_Sob']-Data2['P2_DE'],c=wtIndex)
D={'rmse':Data2['RMSE_Sob']-Data2['RMSE_DE'],'P2':Data2['P2_Sob']-Data2['P2_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P2']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P2']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P2']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P2']<0)])

LC=len(df[(df['rmse']<0)&(df['P2']==0)])
RC=len(df[(df['rmse']>0)&(df['P2']==0)])
UC=len(df[(df['rmse']==0)&(df['P2']>0)])
LoC=len(df[(df['rmse']==0)&(df['P2']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,2,str(UC));plt.text(0,-6,str(LoC));
plt.text(-1.25,2,str(LUQ));plt.text(-1.25,-6,str(LLQ));plt.text(0.75,2,str(RUQ));plt.text(0.75,-6,str(RLQ));

plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2-DE P2')

plt.subplot(2,2,3)
plt.scatter(Data2['RMSE_Sob']-Data2['RMSE_DE'],Data2['Phint_Sob']-Data2['Phint_DE'],c=wtIndex)
D={'rmse':Data2['RMSE_Sob']-Data2['RMSE_DE'],'Phint':Data2['Phint_Sob']-Data2['Phint_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['Phint']>0)])
LLQ=len(df[(df['rmse']<0)&(df['Phint']<0)])
RUQ=len(df[(df['rmse']>0)&(df['Phint']>0)])
RLQ=len(df[(df['rmse']>0)&(df['Phint']<0)])

LC=len(df[(df['rmse']<0)&(df['Phint']==0)])
RC=len(df[(df['rmse']>0)&(df['Phint']==0)])
UC=len(df[(df['rmse']==0)&(df['Phint']>0)])
LoC=len(df[(df['rmse']==0)&(df['Phint']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,40,str(UC));plt.text(0,-100,str(LoC));
plt.text(-1.25,40,str(LUQ));plt.text(-1.25,-100,str(LLQ));plt.text(0.75,40,str(RUQ));plt.text(0.75,-100,str(RLQ));


plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol Phint-DE Phint')

plt.subplot(2,2,4)
plt.scatter(Data2['RMSE_Sob']-Data2['RMSE_DE'],Data2['P2O_Sob']-Data2['P2O_DE'],c=wtIndex)
D={'rmse':Data2['RMSE_Sob']-Data2['RMSE_DE'],'P2O':Data2['P2O_Sob']-Data2['P2O_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P2O']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P2O']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P2O']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P2O']<0)])

LC=len(df[(df['rmse']<0)&(df['P2O']==0)])
RC=len(df[(df['rmse']>0)&(df['P2O']==0)])
UC=len(df[(df['rmse']==0)&(df['P2O']>0)])
LoC=len(df[(df['rmse']==0)&(df['P2O']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,7,str(UC));plt.text(0,-12,str(LoC));
plt.text(-1.25,7,str(LUQ));plt.text(-1.25,-12,str(LLQ));plt.text(0.75,7,str(RUQ));plt.text(0.75,-12,str(RLQ));
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2O-DE P2O')

plt.colorbar()

plt.show()

###################################  GRAPH based on P2O Change Category with sorted index
#NewData=pd.DataFrame()
Data12=Data[(Data['P2O_DE']>14)].reset_index(drop=0)
ADATIndex2=[]
FL6=np.mean([x for x in Data12['OSite9'] if x>0])
FL7=np.mean([x for x in Data12['OSite10'] if x>0])
PR6=np.mean([x for x in Data12['OSite11'] if x>0])
Mean=[FL6,FL7,PR6]
for i in xrange(len(Data12)):
    val1=Data12.iloc[i]
    adat=[val1['OSite9'],val1['OSite10'],val1['OSite11']]
    adat1=[x for x in adat if x>0]
    if len(adat)>0:
        ADATIndex2.append(sum([adat[i]-Mean[i] for i in xrange(len(adat)) if adat[i]>0])/len(adat1))

Data12['ADATIndex2']=ADATIndex2
Data12=Data12.sort(['ADATIndex2'])
wtIndex=Data12['ADATIndex2']
plt.figure(6)
plt.subplot(2,2,1)

plt.scatter(Data12['RMSE_Sob']-Data12['RMSE_DE'],Data12['P1_Sob']-Data12['P1_DE'],c=wtIndex)
D={'rmse':Data12['RMSE_Sob']-Data12['RMSE_DE'],'P1':Data12['P1_Sob']-Data12['P1_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P1']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P1']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P1']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P1']<0)])

LC=len(df[(df['rmse']<0)&(df['P1']==0)])
RC=len(df[(df['rmse']>0)&(df['P1']==0)])
UC=len(df[(df['rmse']==0)&(df['P1']>0)])
LoC=len(df[(df['rmse']==0)&(df['P1']<0)])
plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,300,str(UC));plt.text(0,-150,str(LoC));
plt.text(-1.25,300,str(LUQ));plt.text(-1.25,-150,str(LLQ));plt.text(0.75,300,str(RUQ));plt.text(0.75,-150,str(RLQ));
plt.axvline(x=0);plt.axhline(y=0)
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P1-DE P1')

plt.subplot(2,2,2)
plt.scatter(Data12['RMSE_Sob']-Data12['RMSE_DE'],Data12['P2_Sob']-Data12['P2_DE'],c=wtIndex)
D={'rmse':Data12['RMSE_Sob']-Data12['RMSE_DE'],'P2':Data12['P2_Sob']-Data12['P2_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P2']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P2']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P2']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P2']<0)])

LC=len(df[(df['rmse']<0)&(df['P2']==0)])
RC=len(df[(df['rmse']>0)&(df['P2']==0)])
UC=len(df[(df['rmse']==0)&(df['P2']>0)])
LoC=len(df[(df['rmse']==0)&(df['P2']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,2,str(UC));plt.text(0,-6,str(LoC));
plt.text(-1.25,2,str(LUQ));plt.text(-1.25,-6,str(LLQ));plt.text(0.75,2,str(RUQ));plt.text(0.75,-6,str(RLQ));

plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2-DE P2')

plt.subplot(2,2,3)
plt.scatter(Data12['RMSE_Sob']-Data12['RMSE_DE'],Data12['Phint_Sob']-Data12['Phint_DE'],c=wtIndex)
D={'rmse':Data12['RMSE_Sob']-Data12['RMSE_DE'],'Phint':Data12['Phint_Sob']-Data12['Phint_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['Phint']>0)])
LLQ=len(df[(df['rmse']<0)&(df['Phint']<0)])
RUQ=len(df[(df['rmse']>0)&(df['Phint']>0)])
RLQ=len(df[(df['rmse']>0)&(df['Phint']<0)])

LC=len(df[(df['rmse']<0)&(df['Phint']==0)])
RC=len(df[(df['rmse']>0)&(df['Phint']==0)])
UC=len(df[(df['rmse']==0)&(df['Phint']>0)])
LoC=len(df[(df['rmse']==0)&(df['Phint']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,40,str(UC));plt.text(0,-100,str(LoC));
plt.text(-1.25,40,str(LUQ));plt.text(-1.25,-100,str(LLQ));plt.text(0.75,40,str(RUQ));plt.text(0.75,-100,str(RLQ));


plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol Phint-DE Phint')

plt.subplot(2,2,4)
plt.scatter(Data12['RMSE_Sob']-Data12['RMSE_DE'],Data12['P2O_Sob']-Data12['P2O_DE'],c=wtIndex)
D={'rmse':Data12['RMSE_Sob']-Data12['RMSE_DE'],'P2O':Data12['P2O_Sob']-Data12['P2O_DE']}
df=pd.DataFrame(D)
LUQ=len(df[(df['rmse']<0)&(df['P2O']>0)])
LLQ=len(df[(df['rmse']<0)&(df['P2O']<0)])
RUQ=len(df[(df['rmse']>0)&(df['P2O']>0)])
RLQ=len(df[(df['rmse']>0)&(df['P2O']<0)])

LC=len(df[(df['rmse']<0)&(df['P2O']==0)])
RC=len(df[(df['rmse']>0)&(df['P2O']==0)])
UC=len(df[(df['rmse']==0)&(df['P2O']>0)])
LoC=len(df[(df['rmse']==0)&(df['P2O']<0)])
plt.axvline(x=0);plt.axhline(y=0)

plt.text(-1.25,0,str(LC));plt.text(0.75,0,str(RC));plt.text(0,7,str(UC));plt.text(0,-12,str(LoC));
plt.text(-1.25,7,str(LUQ));plt.text(-1.25,-12,str(LLQ));plt.text(0.75,7,str(RUQ));plt.text(0.75,-12,str(RLQ));
plt.xlabel('Sobol-DE RMSE');plt.ylabel('Sobol P2O-DE P2O')

plt.colorbar()

plt.show()



