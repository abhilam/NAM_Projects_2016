import numpy as np
import scipy
from shapely.geometry import Point
from scipy.spatial import Delaunay
import pandas as pd
import matplotlib.pyplot as plt
from shapely.geometry import Polygon
import csv
import os
from scipy.spatial import ConvexHull
import matplotlib.pyplot as plt
#from mpl_toolkits.mplot3d import Axes3D
from descartes import PolygonPatch
from shapely.geometry import MultiLineString
from shapely.ops import cascaded_union, polygonize
#import json
from matplotlib.collections import LineCollection
import math
import matplotlib.pyplot as mpl

mpl.rcParams['font.size'] = 16
mpl.rc('font', family='sans-serif')

os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Codes_NAM/')

Path='/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Codes_NAM/'
DataDESOB=pd.read_csv('DE_SOBOL_Parms_FL67PR6.csv',sep=',',skiprows=1,header=0)
DataDESOB2=pd.read_csv('NAM_Output_FL67PR6_DE.csv',sep=',',skiprows=0,header=0)

DataDESOB['diffRMSE']=DataDESOB['RMSE_Sob']-DataDESOB['RMSE_DE']
dat=DataDESOB[DataDESOB['diffRMSE']>0].reset_index(drop=0)


for k in xrange(1):
    #k=0

    Fnme=Path+'NAM_Output_FL67PR6_DE.csv'#'Output_4Parms_NAM.csv'
    SiteName1=['FL7']#['NY6','NC6','MO6','IL6','FL6']
    SiteName2=['PR6']#['NY7','NC7','MO7','IL7','FL7']
    b=['Site10']#['Site1','Site3','Site5','Site7','Site9']
    ba=['Site11']#['Site2','Site4','Site6','Site8','Site10']
    col=['ro','g.','co','yo','mo']
    abcd=[11]#[0,2,4,6,8]; ##[Fl6=10,Fl7=11,PR6=12]
    bacd=[12]#[1,3,5,7,9]#Output_4Parms_NAM_NC6NC7


#    Data=open(Path+'NAM_Output_FL67PR6_DE.csv','rb');#SimList_4Parms_ADAT_final
#    Data=csv.reader(Data,delimiter=',')
#    next(Data,None)
#    points_sob=np.ndarray(shape=(5460,2))
#    i=0
#    for row in Data:
#        points_sob[i][0]=(float(row[abcd[k]]))
#        points_sob[i][1]=(float(row[bacd[k]]))
#        i+=1



    ##### THis can be deleted ifnot needed

    Data2=open(Path+'SimList_4Parms_ADAT_final.csv','rb');#SimList_4Parms_ADAT_final#Output_4Parms_NAM_FLPR.csv','rb'
    Data2=csv.reader(Data2,delimiter=',')
    next(Data2,None)
    points_sob1=np.ndarray(shape=(32400070,2))#5457
    i=0
    for row in Data2:

        points_sob1[i][0]=(float(row[9]))# change k vaue accordingly based on the input dayta [17=FL6,18=FL7,19=PR6]
        points_sob1[i][1]=(float(row[10]))#[if sobol data 8=FL6,9-FL7, 10==PR6 and ]
        i+=1

    ###########


   # This is simulated part
    val1=pd.read_csv(Fnme,header=0,sep=',')
    val1=val1[val1['Pop']<28].reset_index()
    val=val1[(val1['O'+b[k]]>0)&(val1['O'+ba[k]]>0)].reset_index(drop=0)

    points_sim=np.ndarray(shape=(len(val),2))
    for i in xrange(len(val)):
        points_sim[i][0]=val['M'+b[k]][i]
        points_sim[i][1]=val['M'+ba[k]][i]

    #val=val1[(val1['O'+b[k]]>0)&(val1['O'+ba[k]]>0)].reset_index(drop=0)
    points_obs=np.ndarray(shape=(len(val),2))
    for i in xrange(len(val)):
        points_obs[i][0]=val['O'+b[k]][i]
        points_obs[i][1]=val['O'+ba[k]][i]

    points=points_sim#points_sob
    tri = Delaunay((points))

    edges = set()
    edge_points = []
    alpha = 0.5

    def add_edge(i, j):
        """Add a line between the i-th and j-th points, if not in the list already"""
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(points[ [i, j] ])
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]

        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)

        # Semiperimeter of triangle
        s = (a + b + c)/2.0

        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))

        circum_r = a*b*c/(4.0*area)

        # Here's the radius filter.
        if circum_r < 1.0/alpha:
            add_edge(ia, ib)
            add_edge(ib, ic)
            add_edge(ic, ia)

    lines = LineCollection(edge_points)
    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))


    ab=cascaded_union(triangles)

    Inside=0
    Point_Inside_X=[];Point_Inside_Y=[]
    Point_Outside_X=[];Point_Outside_Y=[]
    for i in xrange(len(points_obs)):
        if ab.contains(Point(points_obs[i,0],points_obs[i,1]))==True:
            Inside+=1
            Point_Inside_X.append(points_obs[i,0]);Point_Inside_Y.append(points_obs[i,1])
        else:
            Point_Outside_X.append(points_obs[i,0]);Point_Outside_Y.append(points_obs[i,1])
            pass
    print Inside,len(points_obs)

    #plt.figure(k)
    #plt.title("Alpha=2.0 Hull")
    #plt.gca().add_patch(PolygonPatch(cascaded_union(triangles), alpha=0.5))
    #plt.gca().autoscale(tight=False)
    #plt.plot(points_obs[:,0], points_obs[:,1], 'r.')
    #plt.plot(points[:,0], points[:,1], 'b.', hold=1)
    #plt.show()

    fig=plt.figure(k)
    plt.title("Phenotyping space_"+SiteName1[k]+'-'+SiteName2[k])

    import shapely
    if type(ab)==shapely.geometry.multipolygon.MultiPolygon:
        print '******'
        for item in ab:
            plt.gca().add_patch(PolygonPatch(cascaded_union(item), alpha=0.7))
    else:plt.gca().add_patch(PolygonPatch(cascaded_union(triangles), alpha=0.7))


    ############ PLOT SOBOL things too This can be deleted if not needed

    points=points_sob1
    tri = Delaunay((points))

    edges = set()
    edge_points = []
    alpha = 0.5

    def add_edge(i, j):
        #Add a line between the i-th and j-th points, if not in the list already
        if (i, j) in edges or (j, i) in edges:
            # already added
            return
        edges.add( (i, j) )
        edge_points.append(points[ [i, j] ])
    # loop over triangles:
    # ia, ib, ic = indices of corner points of the triangle
    for ia, ib, ic in tri.vertices:
        pa = points[ia]
        pb = points[ib]
        pc = points[ic]

        # Lengths of sides of triangle
        a = math.sqrt((pa[0]-pb[0])**2 + (pa[1]-pb[1])**2)
        b = math.sqrt((pb[0]-pc[0])**2 + (pb[1]-pc[1])**2)
        c = math.sqrt((pc[0]-pa[0])**2 + (pc[1]-pa[1])**2)

        # Semiperimeter of triangle
        s = (a + b + c)/2.0

        # Area of triangle by Heron's formula
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))

        circum_r = a*b*c/(4.0*area)

        # Here's the radius filter.
        if circum_r < 1.0/alpha:
            add_edge(ia, ib)
            add_edge(ib, ic)
            add_edge(ic, ia)

    lines = LineCollection(edge_points)
    m = MultiLineString(edge_points)
    triangles = list(polygonize(m))


    ab=cascaded_union(triangles)

#    Inside=0
#    Point_Inside_X=[];Point_Inside_Y=[]
#    Point_Outside_X=[];Point_Outside_Y=[]
#    for i in xrange(len(points_obs)):
#        if ab.contains(Point(points_obs[i,0],points_obs[i,1]))==True:
#            Inside+=1
#            Point_Inside_X.append(points_obs[i,0]);Point_Inside_Y.append(points_obs[i,1])
#        else:
#            Point_Outside_X.append(points_obs[i,0]);Point_Outside_Y.append(points_obs[i,1])
#            pass
#    print Inside,len(points_obs)



    fig=plt.figure(k)
    plt.title("Phenotyping space_"+SiteName1[k]+'-'+SiteName2[k])

    import shapely
    if type(ab)==shapely.geometry.multipolygon.MultiPolygon:
        print '******'
        for item in ab:
            plt.gca().add_patch(PolygonPatch(cascaded_union(item),alpha=0.3 ))
    else:plt.gca().add_patch(PolygonPatch(cascaded_union(triangles), alpha=0.3))
    ##############################

    #except:'AssertionError'
    plt.gca().autoscale(tight=False)
    plt.plot(Point_Inside_X,Point_Inside_Y, 'y.')
    plt.plot(Point_Outside_X,Point_Outside_Y, 'r.')
    plt.annotate("Inside="+str(Inside),xy=(60,110))
    plt.annotate("Outside="+str(len(points_obs)-Inside),xy=(60,105))

    #plt.plot(dat['OSite9'],dat['OSite10'],'.c')
    #plt.plot(DataDESOB2['MSite9'],DataDESOB2['MSite10'],'.c')

    plt.xlim(40,140);plt.ylim(40,140)

    #plt.savefig("Concave_Hull_Phenotyping space_"+SiteName1[k]+'-'+SiteName2[k]+'.eps',dpi=900)

plt.show()