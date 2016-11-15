
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/')

Data=pd.read_csv('Output_4Parms_NAM.csv',header=0,skiprows=0,sep=',')
Data_Ties=Data[(Data['No_Tie']!=0)&(Data['No_Tie']<1000)].reset_index(drop=0)

Data_Ties=Data_Ties[Data_Ties['Pop_No']<28] # Remove 28 Population


Data_NoTies=Data[Data['No_Tie']==0].reset_index(drop=0)
plt.figure('Family_Ties')
plt.scatter(Data_Ties['Pop_No'],Data_Ties['No_Tie']);
plt.xlabel('RIL_Family');plt.ylabel('No_Ties');plt.title('RIL_Family vs No_Ties')

####################
fig=plt.figure(12)
ax = fig.add_subplot(111)

POP=pd.unique(Data_Ties['Pop_No'])
maxTies_Pop=[]
for item in POP:
    val=Data_Ties[Data_Ties['Pop_No']==item].reset_index(drop=0)
    maxTies_Pop.append(np.max(val['No_Tie']))
sortedPOP_maxTies=[x for (y,x) in sorted(zip(maxTies_Pop,POP))]


a=1
avgSY_POP=[]

for item in reversed(sortedPOP_maxTies):
    data=Data_Ties[Data_Ties['Pop_No']==item].reset_index(drop=0)
    avgSY_POP.append(np.mean(data['No_Sim']))

    plt.scatter([a]*len(data),data['No_Tie'])
    a+=1
plt.xlabel('RIL Family')
ax.set_ylim(0,700)
ax.set_ylabel('Number of Equifinal Points')
ax2 = ax.twinx()
ax2.set_ylim(1,11)

ax2.set_ylabel('Average Number of Site Year')
plt.plot(range(1,len(avgSY_POP)+1),avgSY_POP,'-*k')
plt.show()






#######################################
plt.figure('Family_NoSY')
plt.scatter(Data_Ties['Pop_No'],Data_Ties['No_Sim'])
plt.xlabel('RIL_Family');plt.ylabel('No_SY');plt.title('RIL_Family vs No_SY')
plt.show()

##########################################
NoLine_Family=[]
NoLine_Family_all=[]
for i in range(1,29):
    TempData=Data_Ties[Data_Ties['Pop_No']==i]
    TempData1=Data[Data['Pop_No']==i]
    NoLine_Family.append(len(TempData['Pop_No']))
    NoLine_Family_all.append(len(TempData1['Pop_No']))

#plt.figure('Bar_NoLine_withinTies')
#plt.bar(range(1,29),NoLine_Family)
#plt.xlabel('RIL_Family');plt.ylabel('No_Line');plt.title('RIL_Family vs No_Line')
#plt.ylim(0,300)

plt.figure('Bar_noLine_all')
plt.bar(range(1,29),NoLine_Family_all,color='y')
plt.xlabel('RIL_Family');plt.ylabel('No_Line');plt.title('RIL_Family vs No_Line')
plt.bar(range(1,29),NoLine_Family,color='b')
plt.xlabel('RIL_Family');plt.ylabel('No_Line');plt.title('RIL_Family vs No_Line')
plt.legend(['line_all','line_withinTies'])
plt.ylim(0,300)

plt.figure('CDF_Ties')
Ties=np.sort(Data_Ties['No_Tie'])
p=1.* np.arange(len(Ties))/(len(Ties)-1)
plt.plot(Ties,p,'b')
plt.xlabel('No_Ties');plt.ylabel('Probabilities');plt.title('CDF_NoTies')
#plt.savefig()
plt.show()
