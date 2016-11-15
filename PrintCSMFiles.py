#!/bin/env python
#Prints maize cultivar and ecotype files use on TACC
import os

class PrintMZCUL():
    
    def __init__(self, path):
        self.f = open(os.path.join(path, 'MZCER045.CUL'), 'w')
        self.f.write('*MAIZE CULTIVAR COEFFICIENTS: MZCER045 MODEL\n')
        self.f.write('@VAR#  VRNAME.......... EXPNO   ECO#    P1    P2    P5    G2    G3 PHINT\n')
        
    def WriteLine(self, i, P1, P2, P5, G2, G3, PHINT):
        #FORMAT for cultivar reads in IPVAR.FOR: A6,1X,A16,7X,A6,6F6.0
        self.f.write('iP0%03d iPlant %03d           . iP0%03d%6.2f%6.4f%6.2f%6.2f%6.4f%6.3f\n' % (i,i,i,P1,P2,P5,G2,G3,PHINT))
        
    def CloseFile(self):
        self.f.close()

class PrintSGCUL():
    
    def __init__(self, path):
        self.f = open(os.path.join(path, 'SGCER045.CUL'), 'w')
        self.f.write('*SORGHUM CULTIVAR COEFFICIENTS: GECER045 MODEL\n')
        self.f.write('@VAR#  VAR-NAME........ EXPNO   ECO#    P1    P2   P2O   P2R PANTH    P3    P4    P5 PHINT    G1    G2 PBASE  PSAT\n')
        
    def WriteLine(self, i, P1, P2, P2O, P2R, PANTH, P3, P4, P5, PHINT, G1, G2):
        #FORMAT for cultivar reads in IPVAR.FOR: A6,1X,A16,7X,A6,18F6.0
        self.f.write('iP0%03d iPlant %03d           . iP0%03d%6.2f%6.2f%6.3f%6.2f%6.2f%6.3f%6.2f%6.2f%6.3f%6.3f%6.4f            \n' % (i,i,i,P1,P2,P2O,P2R,PANTH,P3,P4,P5,PHINT,G1,G2))
        
    def CloseFile(self):
        self.f.close()
    
class PrintMZECO():
    
    def __init__(self, path):
        self.f = open(os.path.join(path,'MZCER045.ECO'), 'w')
        self.f.write('*MAIZE ECOTYPE COEFFICIENTS: GECER045 MODEL\n')
        self.f.write('@ECO#  ECONAME.........  TBASE TOPT  ROPT  P20   DJTI  GDDE  DSGFT  RUE   KCAN  TSEN  CDAY\n')
        
    def WriteLine(self, i, TBASE, TOPT, ROPT, P20, DJTI, GDDE, DSGFT, RUE, KCAN):
        #FORMAT for ecotype reads in MZ_PHENOL.FOR: A6,1X,A16,1X,9(1X,F5.1)
        self.f.write('iP0%03d iP_eco%03d         %5.3f %5.2f %5.2f %5.2f %5.3f %5.3f %5.1f %5.3f %5.3f\n' % (i,i,TBASE,TOPT,ROPT,P20,DJTI,GDDE,DSGFT,RUE,KCAN))
        
    def CloseFile(self):
        self.f.close()

class PrintSGECO():
    
    def __init__(self, path):
        self.f = open(os.path.join(path,'SGCER045.ECO'), 'w')
        self.f.write('*SORGHUM ECOTYPE COEFFICIENTS: GECER045 MODEL\n')
        self.f.write('@ECO#  ECONAME.........  TBASE  TOPT  ROPT  GDDE   RUE  KCAN  STPC  RTPC TILFC\n')
        
    def WriteLine(self, i, TBASE, TOPT, ROPT, GDDE, RUE, KCAN, STPC, RTPC, TILFAC):
        #FORMAT for ecotype reads in SG_CERES.FOR: A6,1X,A16,1X,8(1X,F5.0)
        self.f.write('iP0%03d iP_eco%03d         %5.3f %5.2f %5.2f %5.3f %5.3f %5.3f %5.3f %5.3f %5.3f\n' % (i,i,TBASE,TOPT,ROPT,GDDE,RUE,KCAN,STPC,RTPC,TILFAC))
        
    def CloseFile(self):
        self.f.close()

if __name__ == '__main__':
    mycul = PrintMZCUL('C:\\temp\\')
    for i in range(1,1000):
        mycul.WriteLine(i,160.0,0.750,780.0,750.0,8.50,49.00)
    mycul.CloseFile()
    
    myeco = PrintMZECO('C:\\temp\\')
    for i in range(1,1000):
        myeco.WriteLine(i,8.0,34.0,34.0,12.5,4.0,6.0,170.0,4.2,0.85)
    myeco.CloseFile()
    
    mycul = PrintSGCUL('C:\\temp\\')
    for i in range(1,1000):
        mycul.WriteLine(i,180.0,180.0*1.2,12.74,10,180.0*3.667,50.0,150.0,700.0,70.0,15.0,5.0)
    mycul.CloseFile()
    
    myeco = PrintSGECO('C:\\temp\\')
    for i in range(1,1000):
        myeco.WriteLine(i,8.0,34.0,34.0,6.0,4.2,0.85,0.6,0.250,0.1)
    myeco.CloseFile()