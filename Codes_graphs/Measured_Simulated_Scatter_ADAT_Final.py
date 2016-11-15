

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pandas.tools.plotting import scatter_matrix
import os
from scipy import stats
import matplotlib.pyplot as mpl
import statsmodels.formula.api as sm

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')

def RMSE(X,Y):
    RotmSq= np.sqrt(sum(((np.array(X))-Y)**2)/len(X))

    return RotmSq


os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/')

fig=plt.figure(1)
ax = fig.add_subplot(111)
site=['NY6','NY7','NC6','NC7','MO6','MO7','IL6','IL7','FL6','FL7','PR6']
Data=pd.read_csv('Output_4Parms_NAM.csv',sep=',',skiprows=0,header=0);
Data=Data[Data['Pop_No']<28].reset_index(drop=0) # This is to remove Pop 28
col=['r','g','b','c','y','m','r','g','b','c','y','m']
mark=['.','.','.','.','.','.','o','v','*','+','x']
X=[];Y=[]
for i in xrange(11):
    val={'X':Data['MSite'+str(i+1)],'Y':Data['OSite'+str(i+1)]}
    val=pd.DataFrame(data=val)
    val=val[val['Y']>0]
    corr=np.corrcoef(val['X'],val['Y'])[0,1]
    X=X+list(val['X']);Y=Y+list(val['Y'])
    plt.scatter(val['X'],val['Y'],color=col[i],marker=mark[i],label=site[i]+'_r='+str(round(corr,2)))
    print RMSE(val['X'],val['Y']),site[i]

    plt.legend(loc=2,ncol=2,prop={'size':12})
    plt.title('Observed vs Simulated Anthesis Days')
    plt.xlabel('Simulated Anthesis Days');plt.ylabel('Observed Anthesis Days')

z = np.polyfit(X,Y,1)
p = np.poly1d(z)
plt.plot(X,p(X),'-r',linewidth=2)
slope, intercept, r_value, p_value, std_err = stats.linregress(X,Y)
Eqn='y=%.6fx+%.6f'%(z[0],z[1])
ax.text(90,50,Eqn,fontsize=12)
x=np.linspace(*ax.get_xlim())
str3='std Obs= '+ str(round(np.std(Y),3))
str4='std Sim= '+ str(round(np.std(X),3))
print str3
print str4
print RMSE(X,Y)
ax.plot(x,x,'--k')
plt.show()




plt.figure(2)
val1={'P1':Data['P1'],'P2':Data['P2'],'PHINT':Data['Phint'],'P2O':Data['P2O']}
val1=pd.DataFrame(data=val1,columns=['P1','P2','PHINT','P2O'])
axes=scatter_matrix(val1,diagonal='hist',marker='.',alpha=0.5,range_padding=0.05  )
#Axes = scatter_matrix(df, alpha=0.2, figsize=(6, 6), diagonal='kde')
fnt=12
plt.setp(axes[0,0].yaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[1,0].yaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[2,0].yaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[3,0].yaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[3,0].xaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[3,1].xaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[3,2].xaxis.get_majorticklabels(), 'size', fnt)
plt.setp(axes[3,3].xaxis.get_majorticklabels(), 'size', fnt)



#plt.setp(axes[0,0],yticks=[150,200,250,300,350,400],yticklabels=['',200,250,300,350,400])

cor=val1.corr(method='pearson')
print cor

plt.show()
# P1 Vs P2
print '######################'

result=sm.ols(formula="P1~ P2",data=val1).fit()
print "P1 Vs P2"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"
print result.params

print '######################'

result=sm.ols(formula="P2~ P1",data=val1).fit()
print "P2 Vs P1"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"
print result.params

print '######################'

result=sm.ols(formula="P1~ PHINT",data=val1).fit()
print "P1 Vs Phint"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"
print result.params

print '######################'

result=sm.ols(formula="P1~ P2O",data=val1).fit()
print "P1 Vs P2O"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"

print result.params

print '######################'

result=sm.ols(formula="P2~ PHINT",data=val1).fit()
print "P2 Vs Phint"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"

print result.params

print '######################'

result=sm.ols(formula="P2~ P2O",data=val1).fit()
print "P2 Vs P2O"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"

print result.params

print '######################'
result=sm.ols(formula="P2O~ PHINT",data=val1).fit()
print "P2O Vs PHINT"
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"

print result.params

print '######################'
result=sm.ols(formula="PHINT~P2O ",data=val1).fit()
print " PHINT Vs P2O "
print result.pvalues
print 'r2=',result.rsquared
print "For Slope"

print result.params
