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
os.chdir('/media/FantomHD/Abhi_Academics/Abhishes_Lamsal_lin/NAME_MAIZE/Check_Optimization/')

#Path='/home/abhi/Desktop/NAME_MAIZE/'
for k in xrange(1):
    #k=0

    Fnme='Output_Optimization_PYCER_Wider_NY67.csv'#'Output_Optimization_DE_NY6NY7_Orig_DSSAT.csv'#'Output_4Parms_NAM.csv'
    SiteName1=['NY6','NC6','MO6','IL6','FL6']
    SiteName2=['NY7','NC7','MO7','IL7','FL7']
    b=['Site1','Site3','Site5','Site7','Site9']
    ba=['Site2','Site4','Site6','Site8','Site10']
    col=['ro','g.','co','yo','mo']
    abcd=[0,2,4,6,8];bacd=[1,3,5,7,9]#Output_4Parms_NAM_NC6NC7

    Data2=open('SimList_4Parms_ADAT_final.csv','rb');#SimList_4Parms_ADAT_final#Output_4Parms_NAM_FLPR.csv','rb'
    Data2=csv.reader(Data2,delimiter=',')
    next(Data2,None)
    points_sob1=np.ndarray(shape=(32400070,2))#5457
    i=0
    for row in Data2:

        points_sob1[i][0]=(float(row[0]))# change k vaue accordingly based on the input dayta [17=FL6,18=FL7,19=PR6]
        points_sob1[i][1]=(float(row[1]))#[if sobol data 8=FL6,9-FL7, 10==PR6 and ]
        i+=1


    Data=open('Output_Optimization_PYCER_Wider_NY67.csv','rb');#SimList_4Parms_ADAT_final#Output_Optimization_DE_NY6NY7_Orig_DSSAT.csv
    Data=csv.reader(Data,delimiter=',')
    next(Data,None)
    points_sob=np.ndarray(shape=(5464,2))#5375
    i=0
    for row in Data:
        points_sob[i][0]=(float(row[9]))
        points_sob[i][1]=(float(row[10]))
        i+=1
   # This is simulated part
    val1=pd.read_csv(Fnme,header=0,sep=',')
    val1=val1[val1['Pop_No']<28].reset_index() # remove 28
    val=val1[(val1['NY6_Obs']>0)&(val1['NY7_Obs']>0)].reset_index(drop=0)
    points_sim=np.ndarray(shape=(len(val),2))
    for i in xrange(len(val)):
        points_sim[i][0]=val['NY6_Sim'][i]
        points_sim[i][1]=val['NY7_Sim'][i]

    val=val1[(val1['NY6_Obs']>0)&(val1['NY7_Obs']>0)].reset_index(drop=0)
    print len(val)
    points_obs=np.ndarray(shape=(len(val),2))
    for i in xrange(len(val)):
        points_obs[i][0]=val['NY6_Obs'][i]
        points_obs[i][1]=val['NY7_Obs'][i]

    points=points_sim
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
    Data_Inside=pd.DataFrame()
    Data_Outside=pd.DataFrame()
    for i in xrange(len(points_obs)):
        if ab.contains(Point(points_obs[i,0],points_obs[i,1]))==True:
            Data_Inside=Data_Inside.append(val.iloc[i])
            Inside+=1
            Point_Inside_X.append(points_obs[i,0]);Point_Inside_Y.append(points_obs[i,1])
        else:
            Point_Outside_X.append(points_obs[i,0]);Point_Outside_Y.append(points_obs[i,1])
            Data_Outside=Data_Outside.append(val.iloc[i])
            pass
    print Inside,len(points_obs)
    InsideDE=Inside
    OutsideDE=len(points_obs)-InsideDE
    Data_Inside.to_csv('DE_NY67_DataInside.csv')
    #Data_Outside.to_csv('DE_NY67_DataOutside.csv')
    dfInside=pd.DataFrame({'NY6':Point_Inside_X,'NY7':Point_Inside_Y})
    #dfInside.to_csv('NY67DE_Inside.csv')
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

    ##########
    points=points_sob1
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
    plt.title("Phenotyping space "+SiteName1[k]+'-'+SiteName2[k])

    import shapely
    if type(ab)==shapely.geometry.multipolygon.MultiPolygon:
        print '******'
        for item in ab:
            plt.gca().add_patch(PolygonPatch(cascaded_union(item), alpha=0.3))
    else:plt.gca().add_patch(PolygonPatch(cascaded_union(triangles), alpha=0.3))
    ##########


    #except:'AssertionError'
    plt.gca().autoscale(tight=False)
    plt.plot(Point_Inside_X,Point_Inside_Y, 'y.')
    plt.plot(Point_Outside_X,Point_Outside_Y, 'r.')
    plt.annotate("Inside="+str(InsideDE),xy=(60,110))
    plt.annotate("Outside="+str(OutsideDE),xy=(60,105))
    plt.xlim(40,140);plt.ylim(40,140)

    #plt.savefig("Concave_Hull_Phenotyping space_"+SiteName1[k]+'-'+SiteName2[k]+'.eps',dpi=900)
plt.xlabel('Days (NY6)')
plt.ylabel('Days (NY7)')
plt.show()