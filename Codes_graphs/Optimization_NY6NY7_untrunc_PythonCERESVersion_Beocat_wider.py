
# CERES-Maize 45 Phenology code
import scipy.optimize as optimize
import time
import subprocess
import os
import math
#from Steve_PSOSimpleFunction import *
import numpy as np
import pandas as pd
import datetime
import csv
from math import *
import sys
csv.field_size_limit(10000000000)

Path2=''#  '/home/abhi/Desktop/NAME_MAIZE/Check_Optimization/Optimization_using_PythonVersion_DSSAT/'
Path3='' #'/home/abhi/Desktop/NAME_MAIZE/Check_Optimization/Optimization_using_PythonVersion_DSSAT/NAM_WTH/'
#

def RMSE(X,Y):
    # X=Observed;Y=Simulated
    SS1=0
    n=0
    for j in xrange(len(X)):
        if X[j]<=0 or Y[j]<=10:continue
        else:n+=1;SS1+=(X[j]-Y[j])**2
    RMSE=math.sqrt(float(SS1)/n)
    return [RMSE, n]
    
    
def TWILEN(XLAT,DOY):
    S1 = sin(XLAT*0.01745)
    C1 = cos(XLAT*0.01745)
    DEC    = 0.4093*sin(0.0172*(DOY-82.2))
    DLV    = ((-S1*sin(DEC)-0.1047)/(C1*cos(DEC)))
    DLV    = max(DLV,-0.87)
    TWILEN = 7.639*acos(DLV)
    return round(TWILEN,6)
    
def ThermalTime(Tmax,Tmin,SRAD,DAYL,LeafNo):
    Tbase=8.0;DOPT=34.;
    if Tmax<Tbase:DT=0.0
    elif Tmin>DOPT:DT=DOPT-Tbase       
    elif (LeafNo<=10.):        
        ACOEF=0.01061*SRAD +0.5902
        TDSOIL=ACOEF*Tmax+(1.0-ACOEF)*Tmin
        TNSOIL=0.36354*Tmax+0.63646*Tmin
        if TDSOIL<Tbase:DT=0.0
        else:
            if TNSOIL<Tbase:TNSOIL=Tbase
            if TDSOIL>DOPT:TDSOIL=DOPT
            TMSOIL=TDSOIL*(DAYL/24.)+TNSOIL*((24.-DAYL)/24.)
            if TMSOIL<Tbase:DT=(Tbase+TDSOIL)/2. - Tbase
            else:DT=(TNSOIL+TDSOIL)/2.0 - Tbase
        DT=min(DT,(DOPT-Tbase))      
    elif Tmin<Tbase or Tmax>DOPT:
        DT=0.0
        for i in range(1,25):
            TH=(Tmax+Tmin)/2. + (Tmax-Tmin)/2. * sin(3.14/12.*i)
            if TH <Tbase:TH=Tbase
            if TH>DOPT:TH=DOPT
            DT+=(TH-Tbase)/24.
    else:DT=(Tmax+Tmin)/2.0 - Tbase
    DT=max(DT,0.0)
    return DT

val=np.genfromtxt(Path2+'DayLen_PHotoper_11SY.csv',names=True,delimiter=',')
#for k in xrange(2):
k=int(os.environ['SGE_TASK_ID'])-1



#Data=pd.read_csv(Path2+'Output_4Parms_NAM_NY6NY7.csv',sep=',',skiprows=0,header=0)
Data=pd.read_csv(Path2+'Observed_ADAT.csv',sep=',',skiprows=0,header=0)
pop=Data['Pop_No'][k];entry=Data['Line_No'][k]

Obs_ADAT=[Data['OSite9'][k],Data['OSite10'][k],Data['OSite11'][k]]

if all(item <0 for item in Obs_ADAT):sys.exit()
Obs_test=[round(item) for item in Obs_ADAT]

#Obs_test=[round(Data['OSite1'][k]),round(Data['OSite2'][k])]


Latt=[42.73,42.73,35.67,35.66,38.89,38.89,40.08,40.08,25.51,25.51,18.001]
DOP=[2006128,2007135,2006122,2007120 ,2006137,2007138,2006128,2007137,2006265,2007282,2006314]
GDDE=6;SDEPTH=2.5;DJTI=4.0;NDAS=0;SUMDTT=0
SiteNme=['NY6','NY7','NC6','NC7','MO6','MO7','IL6','IL7','FL6','FL7','PR6']
WTHFnme=['NYAU0601.WTH','NYAU0701.WTH','NCCL0601.WTH','NCCL0701.WTH','MOCO0601.WTH','MOCO0701.WTH','ILUR0601.WTH','ILUR0701.WTH','FLHO0601.WTH','FLHO0701.WTH','PRPO0601.WTH']
Start=time.time()
            
    
abc=[[]]
def NelderMead_Optimize(x):
    #cult=5467      
    P1=x[0];P2=x[1];Phint=x[2];P2O=x[3]

    #ADAT_frm_SObol=[Data1['MSite1'][cult],Data1['MSite2'][cult],Data1['MSite3'][cult],Data1['MSite4'][cult],Data1['MSite5'][cult],Data1['MSite6'][cult],
    #Data1['MSite7'][cult],Data1['MSite8'][cult],Data1['MSite9'][cult],Data1['MSite10'][cult],Data1['MSite11'][cult]]
    ADAT=[]
    for site in xrange(2):#len(WTHFnme)):
        #site=2
        PHP=[]
        for item in val['DAY_'+SiteNme[site]]:
            PHP.append(TWILEN(Latt[site],item))
        #print PHP 
        #PHP=val[SiteNme[site]+'_TWIL']#6#3 #  Photoperiod value from DSSAT
        DAYLen=val[SiteNme[site]+'_DAYLEN'] # Daylength value from DSSAT
        # Read Weather File and Store TMAX, TMIN, RAIN
        Data=open(Path3+WTHFnme[site],'r')
        Date=[];SRAD=[];TMAX=[];TMIN=[]
        line=0
        counter=999
        for item in Data.readlines():
            #print WTHFnme[site][4:6]+str(DOP[site])[4:8]
            if item.startswith(WTHFnme[site][4:6]+str(DOP[site])[4:8]):
                counter=line
                ##print counter
            if line >=counter:
                Date.append(int(item[0:6]))
                SRAD.append(float(item[7:11]))
                TMAX.append(float(item[13:17]))
                TMIN.append(float(item[19:23])) 
                #print line, TMAX[-1]
            line+=1    
        
        DTT=0;CUMPH=0.514;LEAFNO=0;STAGE=7
        l=0
        for k in xrange(140):    
            if STAGE==7.0:
                DTT= ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                SUMDTT=0
                #print DTT,SUMDTT+DTT,LEAFNO
                STAGE=8;l+=1
            
            if STAGE==8: #(Determine Germination Date)
                DTT= ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                SUMDTT=0
                #print DTT,SUMDTT+DTT,LEAFNO
                #print'Germination on', l,' Days','**********************************'
                P9=45.0+GDDE*SDEPTH;STAGE=9
                
            if STAGE==9:#(Determine Emergence Date)
                l+=1
                SUMDTT+=  ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                #print l,ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO) ,SUMDTT ,LEAFNO
                if SUMDTT>=P9:
                    #print 'Emergence on',l,' Days','**********************************'
                    SUMDTT=SUMDTT-P9 
                    LEAFNO=1;STAGE=1
        
            if STAGE==1:# (Emergence to Juvenile Phase)
                PC=1.0
                if CUMPH<5.0:PC=0.66+0.068*CUMPH
                DTT1=ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                TI=DTT1/(Phint*PC);CUMPH+=TI;XN=CUMPH+1.;LEAFNO=int(XN)
                DTT=ThermalTime(TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1],LEAFNO);##print '*****',LEAFNO,DTT
                SUMDTT+=DTT
                #print '***'
                #print 'CUMPH',CUMPH, 'DTT1=',DTT1,'LN',LEAFNO,TMAX[l],TMIN[l],SRAD[l],DAYLen[l]
                #print 'DTT=',DTT,'SUMDT=',SUMDTT,'P1',P1,'LN=',LEAFNO,TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1]#,TMAX[NDAS],TMIN[NDAS],SRAD[NDAS],DAYLen[NDAS],#LEAFNO
                l+=1
                if SUMDTT>=P1:
                    #print 'End of Juvenile on',l, ' Days','**********************************'
                    STAGE=2;
                    SIND=0.0

            if STAGE==2:#STAGE 2 [End of Juvenile to Tassel Initiation]
                PC=1.0
                if CUMPH<5.0:
                    PC=0.66+ 0.068*CUMPH
                DTT1=ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                TI=DTT1/(Phint*PC);
                CUMPH+=TI;XN=CUMPH+1.; 
                LEAFNO=int(XN)
                DTT=ThermalTime(TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1],LEAFNO);##print '*****',LEAFNO,DTT
                SUMDTT+=DTT
                #print '***'
                #print 'CUMPH',CUMPH, 'DTT1=',DTT1,'LN',LEAFNO,TMAX[l],TMIN[l],SRAD[l],DAYLen[l]
                #print 'DTT=',DTT,'SUMDT=',SUMDTT,'LN=',LEAFNO,TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1]#,TMAX[NDAS],TMIN[NDAS],SRAD[NDAS],DAYLen[NDAS],#LEAFNO
                l+=1
                if PHP[l]>P2O:TWIL=PHP[l]; RATEIN=1.0/(DJTI+P2*(TWIL-P2O));#print 'l',l
                else:RATEIN=1.0/DJTI
                PDTT=1.0
                SIND+=RATEIN*PDTT
                
                #print 'SIND',SIND,'RATEIN',RATEIN,'P2O',P2O,'TWIL',TWIL,'P2',P2
                if SIND>=1:
                    
                    #print 'end of Tassel Initiation on', l, ' Days','**********************************'
                    #print '**',ThermalTime(TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1],LEAFNO),SUMDTT,LEAFNO,TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1]
                    TLNO=(SUMDTT)/(Phint*0.5)+5.0
                    P3=((TLNO+0.5)*Phint)-(SUMDTT)
                    #print 'P3',P3,'TLNO',TLNO,'Phint',Phint,'SUMDTT',SUMDTT,
                    SUMDTT=0;STAGE=3## Initialize for Stage 3
                    
            if STAGE==3:
                PC=1.0
                if CUMPH<5.0:
                    PC=0.66+ 0.068*CUMPH
                DTT1=ThermalTime(TMAX[l],TMIN[l],SRAD[l],DAYLen[l],LEAFNO)
                TI=DTT1/(Phint*PC);
                CUMPH+=TI
                if SUMDTT>P3-(2*Phint):CUMPH=CUMPH-TI
                XN=CUMPH+1.;LEAFNO=int(XN)
                DTT=ThermalTime(TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1],LEAFNO)
                SUMDTT+=DTT
                #print '***'
                #print 'CUMPH',CUMPH, 'DTT1=',DTT1,'LN',LEAFNO,TMAX[l],TMIN[l],SRAD[l],DAYLen[l]
                #print 'DTT=',DTT,'SUMDT=',SUMDTT,'LN=',LEAFNO,TMAX[l+1],TMIN[l+1],SRAD[l+1],DAYLen[l+1]#,TMAX[NDAS],TMIN[NDAS],SRAD[NDAS],DAYLen[NDAS],#LEAFNO
                l+=1
                if l>=139:
                    ADAT.append(l)
                    break
                if SUMDTT>=P3:
                    #ADT=l
                    ADAT.append(l)
                    #print 'Anthesis Days Occur at', l, ' Days','**********************************'
                    #print 'TLNO',XN
                    #print '************************'
                    #print '*************************'
                    break
    abc[0]=ADAT
    #print Obs_ADAT,ADAT
    value=RMSE(Obs_ADAT,ADAT)
    if np.array_equal(ADAT,Obs_test):
        print 'Pop','line','Parms','RMSE','Obs','Simul11'
        print '[',',',pop,',', entry,',',value[0],',', x[0],',',x[1],',',x[2],',',x[3],',',Obs_ADAT[0],',',Obs_ADAT[1],',',Obs_ADAT[2],','abc[0][0],',',abc[0][1],',',abc[0][2]
        
        sys.exit()
    
    #value=RMSE(Obs_ADAT,ADAT)

    #global_min[0]=value[0]
    return value[0]

############### Differential Evolution
bounds=[(75,600),(0,6),(20,150),(6,21)]#,(500,16,75,6,.201)]
Start=time.time()
NewOpt=optimize.differential_evolution(NelderMead_Optimize, bounds,maxiter=5000, popsize=400,polish=True)
end=time.time()
#print end-Start , '_Second'
#print " DIFFERENTIAL EVOLUTION OUTPUT"
#print "========"
#print "Best Objective Function Value = ",NewOpt.fun
#print "Decision variables: X* = \n", NewOpt.x
#print  "number of iteration performed by the optimizer = ", NewOpt.nit
#print "number of evaluation of the objective functions and of its jacobian : ", NewOpt.nfev
print 'Pop','line','Parms','RMSE','Obs','Simul'
print '[',',',pop,',', entry,',',NewOpt.fun,',', NewOpt.x[0],',',NewOpt.x[1],',',NewOpt.x[2],',',NewOpt.x[3],',',Obs_ADAT[0],',',Obs_ADAT[1],',',Obs_ADAT[2],','abc[0][0],',',abc[0][1],',',abc[0][2]
