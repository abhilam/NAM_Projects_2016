# -*- coding: utf-8 -*-
"""
Created on Tue Sep  6 11:55:37 2016

@author: abhi

Email: abhilam@ksu.edu
Purpose:


Kansas State University
Manhattan, KS

"""

import numpy as np
from read_array import read_array
import os
import pandas as pd
import matplotlib.pylab as plt
os.chdir("/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Inputs/")
#Path='C:\Users\user1\Desktop\Abhishes_lamsal\Acedemics\NAM_desktop\PY\\'
data_type2=np.dtype([('pop','int32'),('entry_num','int32'),('dts','float64'),('dta','float64'),('asi','float64'),('nme','string'),('site','int32')])
ObsData=read_array( 'allnamflowerblupbyenv.csv', data_type2, skip=1, missing='-99')
ObsData=ObsData[ObsData['pop']<28]
#Create matrix for observed data
Observed=[[[-99 for site in xrange(11)] for entryno in xrange(282)] for pop in xrange(27)]
for i in xrange(len(ObsData)):#xrange(len(ObsData)):
    Observed[ObsData["pop"][i]-1][ObsData["entry_num"][i]-1][ObsData["site"][i]-1]=ObsData["dta"][i]
N=0.
pop=[]
Line=[]
a=[]
b=[]
plt.subplot(211)
for p in xrange(27):
    c=0
    for l in xrange(282):
        if (Observed[p][l])!=[-99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99]:
            N+=1
            c+=1
            pop.append(p+1)
            Line.append(l+1)
        else:
            continue
    a.append(p+1)
    b.append(c)
    plt.text(p+0.5,c+5,str(c))

plt.bar(a,b,align='center')
plt.xlim(0,29)
plt.tight_layout()
df=pd.DataFrame({'pop':pop,'Line':Line})

df.to_csv('Pop_line')


a1=[]
b1=[]
plt.subplot(212)

popn=['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27']
for item in popn:
    Dat=open('MZCER045.cul','r')
    c1=0
    for line in Dat.readlines():
        #bre
        if line[0:3]=='N'+item:
            #print line

            c1+=1
    plt.text(int(item)-0.5,c1+5,str(c1))
    a1.append(int(item))
    b1.append(c1)
plt.bar(a1,b1,align='center')
plt.xlim(0,29)
bac=0
## print number of plantings on each siteyear
sy=['NY6','NY7','NC6','NC7','MO6','MO7','IL6','IL7','FL6','FL7','PR6']
for i in xrange(11):
    print len(ObsData[ObsData['site']==i+1]),sy[i]
    bac+=len(ObsData[ObsData['site']==i+1])

print "#######"
os.chdir("/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/")

ObservedADAT=pd.read_csv('Output_4Parms_NAM.csv',sep=',',skiprows=0,header=0);
ObservedADAT=ObservedADAT[ObservedADAT['Pop_No']<28]
abc=0
for i in xrange(11):
    Dat=ObservedADAT['OSite'+str(i+1)]
    print len(Dat[Dat>0]),sy[i]
    abc+=len(Dat[Dat>0])

print 'abc',abc
print bac,'bac'
