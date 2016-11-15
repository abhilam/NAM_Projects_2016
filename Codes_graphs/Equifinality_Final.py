

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as mpl
from math import *
from scipy.stats import mode
mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/')
# THis will plot Number of line vs Number of Equifinal points
fig=plt.figure(1)
ax = fig.add_subplot(211)

Data=pd.read_csv('Output_4Parms_NAM.csv',sep=',',skiprows=0,header=0);
Data=Data[Data['Pop_No']<28]

Val=Data[(Data['No_Tie']>=1)].reset_index();#&(Data['No_Tie']<=500)
print len(Val)

Ties=np.sort(Val['No_Tie'].unique())
Ties_freq=[]
freq=0
avgSY=[]
for item in Ties:
    #print i
    if item>=40:
        SZ=np.shape(Val[Val['No_Tie']==item])
        ab=Val[Val['No_Tie']>=40].reset_index(drop=0)
        #avgSY.append(mode(ab['No_Sim'])[0][0])
        avgSY.append(np.mean(ab['No_Sim']))

        freq= freq+SZ[0]
        #print freq

    else:
        SZ=np.shape(Val[Val['No_Tie']==item])
        ab=Val[Val['No_Tie']==item].reset_index(drop=0)
        #avgSY.append(median(ab['No_Sim'])[0][0])
        avgSY.append(np.mean(ab['No_Sim']))
        #print SZ[0],'yht'
        if SZ[0]==0:
           Ties_freq.append(0)
        Ties_freq.append(SZ[0])

#print Ties
print sum(Ties_freq)
print 'freq',freq
Ties_freq=np.concatenate((Ties_freq,[freq]))

ax.bar(Ties[0:len(Ties_freq)-1],Ties_freq[0:len(Ties_freq)-1],align='center')
plt.xlabel('Number of Equifinal Points')
plt.ylabel('Number of Lines')
labels=[item.get_text() for item in ax.get_xticklabels()]
labels=['0','5','10','15','20','25','30','35','']
ax.set_xticklabels(labels)
plt.xlim(0,41)
print sum(Ties_freq[0:len(Ties_freq)-1])

ax2 = ax.twinx()
ax2.set_ylabel('Average Number of Site Year')
ax2.plot(Ties[0:37],avgSY[0:37],'.-k')
ax2.set_ylim(1,11)
plt.xlim(0,41)
plt.show()

print sum(Ties_freq)

##############################
#fig=plt.figure(2)
mpl.rcParams['font.size'] = 16
ax3 = fig.add_subplot(212)
Ties=np.sort(Val['No_Tie'].unique())
Ties1=[]
Ties_freq=[]
freq=0
avgSY=[]
for item in Ties:
    #print i
    if item>=40:
        SZ=np.shape(Val[Val['No_Tie']==item])
        ab=Val[Val['No_Tie']>=item].reset_index(drop=0)
        #avgSY.append(mode(ab['No_Sim'])[0][0])
        avgSY.append(np.mean(ab['No_Sim']))

        #print SZ[0],'kjk'
        Ties_freq.append(SZ[0])
        Ties1.append(item)

    else:
        continue

#        SZ=np.shape(Val[Val['No_Tie']==item])
#        ab=Val[Val['No_Tie']==item].reset_index(drop=0)
#        #avgSY.append(median(ab['No_Sim'])[0][0])
#        avgSY.append(np.mean(ab['No_Sim']))
#        print SZ[0],'yht'
#        if SZ[0]==0:
#           Ties_freq.append(0)
#        Ties_freq.append(SZ[0])

#Ties_freq=np.concatenate((Ties_freq,[freq]))

#ax3.bar(range(0,len(Ties_freq)),Ties_freq[0:len(Ties_freq)],align='center')
#plt.xlabel('Number of Equifinal Points')
#plt.ylabel('Number of Lines')
ax4 = ax3.twinx()
ax4.plot(range(0,len(Ties_freq)),avgSY,'.-k')
ax4.set_ylim(1,11)
ax3.set_xlim(0,len(Ties1))
plt.xticks(np.arange(0,len(Ties1)+1,1),fontsize=10)
ax3.set_xticklabels(Ties1,rotation=90)
ax3.set_yticklabels([0,1,2,3,4,5])

#plt.tight_layout()
plt.show()
print sum(Ties_freq)