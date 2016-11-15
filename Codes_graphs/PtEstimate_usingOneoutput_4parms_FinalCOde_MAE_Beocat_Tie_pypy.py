import time

import csv
import operator
import math
from decimal import *
import os
import time

Start=time.clock()
B=time.clock()
###############
def RMSE(X,Y):
    SS1=0
    n=0
    for j in xrange(11):
        if X[j]<=0 or Y[j]==-99:continue
        else:n+=1;SS1+=(X[j]-Y[j])**2
    RMSE=math.sqrt(float(SS1)/n)
    return [RMSE, n]

####################
###############
def MAE(X,Y):
    SS1=0
    n=0
    for j in xrange(11):
        if X[j]<=0 or Y[j]==-99:continue
        else:n+=1;SS1+=abs(X[j]-Y[j])
    MAE=(float(SS1)/n)
    return [MAE, n]

####################

Path=''#C:\Users\user1\Desktop\Abhishes_lamsal\Acedemics\NAM_desktop\Second_RUn\PointEstimate\\'
Obs_Data= {'Pop':[],'Line':[],'NY6':[],'NY7':[],'NC6':[],'NC7':[],'MO6':[],'MO7':[],'IL6':[],'IL7':[],'FL6':[],'FL7':[],'PR6':[],}
with open('Observed_ADAT.csv','rb') as csvfile:
    csvreader=csv.reader(csvfile);next(csvreader,None)
    for row in csvreader:
        Obs_Data['Pop'].append(int(row[0]));Obs_Data['Line'].append(float(row[1]));Obs_Data['NY6'].append(float(row[2]))
        Obs_Data['NY7'].append(float(row[3]));Obs_Data['NC6'].append(float(row[4]));Obs_Data['NC7'].append(float(row[5]))
        Obs_Data['MO6'].append(float(row[6]));Obs_Data['MO7'].append(float(row[7]));Obs_Data['IL6'].append(float(row[8]))
        Obs_Data['IL7'].append(float(row[9]));Obs_Data['FL6'].append(float(row[10]));Obs_Data['FL7'].append(float(row[11]))
        Obs_Data['PR6'].append(float(row[12]))

#for k in xrange(1):# Loop Over Line
k=1#int(os.environ['SGE_TASK_ID'])-1

# Initialise Empty List to store Data
No_observed_data1=          [] # Store Observed ADAT Data for all site years
No_Model_result1=           [] # Store Simulated ADAT Data for all site years
No_Simulation1=             [] # Store number of data points used to calculate RMSE
RMSEList1=                  [] # Store Best RMSE
Position_BestRMSE1=         [] # Store position of Parameters that gives Best RMSE
Parms_BestRMSE=             [] # Store Parameters that gives Best RMSE
Line_No1=[];Pop_No1=        [] # Store Line and Population
Tie1=                       [] # Store how many number of Ties 
####################################
SimList_Data = open('SimList_4Parms_ADAT_final.csv','rb');SimList_Data=csv.reader(SimList_Data);next(SimList_Data,None)
ParmCombn=open(Path+'ParmCombn_4Parms.csv','rb');ParmCombn=csv.reader(ParmCombn);next(ParmCombn)       
count1=0.;BestRMSE1=123456779876890.000;No_Sim1=[];NoMaxSim=0; #RMSE1=0.;
Observed= [Obs_Data['NY6'][k],Obs_Data['NY7'][k],Obs_Data['NC6'][k],Obs_Data['NC7'][k],Obs_Data['MO6'][k],Obs_Data['MO7'][k],Obs_Data['IL6'][k],Obs_Data['IL7'][k],Obs_Data['FL6'][k],Obs_Data['FL7'][k],Obs_Data['PR6'][k]]
Pop_Line=[Obs_Data['Pop'][k],Obs_Data['Line'][k]]
i=0
for i in xrange(32400070):      
    Sim_ADAT=SimList_Data.next()
    SimList= [float(Sim_ADAT[0]),float(Sim_ADAT[1]),float(Sim_ADAT[2]),float(Sim_ADAT[3]),float(Sim_ADAT[4]),float(Sim_ADAT[5]),float(Sim_ADAT[6]),float(Sim_ADAT[7]),float(Sim_ADAT[8]),float(Sim_ADAT[9]),float(Sim_ADAT[10])]
    # This is for maximum number of matches
    #SimList[2]=-99;SimList[3]=-99;SimList[4]=-99;SimList[5]=-99;SimList[6]=-99
    #SimList[7]=-99;SimList[8]=-99;SimList[9]=-99;SimList[10]=-99
    
    Parameters=ParmCombn.next()
    Parms=[float(Parameters[0]),float(Parameters[1]),float(Parameters[2]),float(Parameters[3])]
    RMSE1=MAE(SimList,Observed)
    if RMSE1[0]==BestRMSE1:
        count1+=1;TiePos.append(i);TieParms.append(Parms);TieSimul.append(SimList)
    if RMSE1[0] <BestRMSE1 and RMSE1[1]>=NoMaxSim:
        TiePos=[];TieParms=[];TieSimul=[]       # This is for storing Ties position and Tie Parameter
        NoMaxSim=RMSE1[1]           ## This is for storing maximum number of data points used in simulation
        count1 =0                   # This is for counting Ties
        BestRMSE1=RMSE1[0]          # Store Best Minimum RMSE
        Position1=i                 # Store position that gives Best Minimum RMSE
        No_Sim1=RMSE1[1]            # Store number of data points used in simulation
        Sim=SimList                 # Store Simulated data that gives Best minimum RMSE
        Parms_Best=Parms            # Store parameters that gives Best RMSE
    i+=1

No_observed_data1.append(Observed)
No_Model_result1.append(Sim)
No_Simulation1.append(No_Sim1)
RMSEList1.append(BestRMSE1)
Position_BestRMSE1.append(Position1)
Parms_BestRMSE.append(Parms_Best)
Line_No1.append(int(Pop_Line[1]))
Pop_No1.append(int(Pop_Line[0]))
Tie1.append(count1)

print 'Pop_No1',',','Line_No1',',','RMSEList1',',','P1',',','P2',',','Phint',',','P2O',',','Tie1',',','No_Simulation1',',','No_Model_result1',',','Position_BestRMSE1',',','No_observed_data1'
#print Pop_No1,',',Line_No1,',', RMSEList1,',',ParmCombn['P1'][Position_BestRMSE1[0]],',',ParmCombn['P2'][Position_BestRMSE1[0]],',',ParmCombn['Phint'][Position_BestRMSE1[0]],',',ParmCombn['P2O'][Position_BestRMSE1[0]],',',Tie1,',',No_Simulation1,',',No_Model_result1,',',Position_BestRMSE1,',',No_observed_data1
print Pop_No1,',',Line_No1,',', RMSEList1,',',Parms_BestRMSE,',',Tie1,',',No_Simulation1,',',No_Model_result1,',',Position_BestRMSE1,',',No_observed_data1

######## This is for Ties Data ################
if len(TiePos)>0:
    for ii in xrange(len(TiePos)):
        print Pop_No1,',',Line_No1,',', RMSEList1,',',TieParms[ii],',',Tie1,',',No_Simulation1,',',TieSimul[ii],',',TiePos[ii],',',No_observed_data1


end=time.clock()
print end-Start

